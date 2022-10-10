import requests
import threading
import json
from FetchData.Image import Image
from GenericFunctions.Logger import Logger
from FetchData.IproxProject import IproxProject
from FetchData.IproxProjects import IproxProjects
from FetchData.IproxNews import IproxNews
from FetchData.IproxStadsloketten import Scraper as IproxStadslokettenScraper


class IproxIngestion:
    """ Ingest projects will call the IPROX-endpoint based on path (url). It will fetch the data in three stages:

        stage 1: Fetch all projects based on path
        stage 2: Fetch all project details based on result from stage 1
        stage 3: Fetch all images based on result from stage 2

        Ingest Projects will skip fetching records based on modification time. (eg. only fetch new records)

        Garbage collecting:

        The garbage collector is initialized with current time. All projects with a last_seen time before current time
        are possibly due for garbage collecting. See details in class IproxGarbageCollector.

        Unique identifiers in Iprox: itmidt
        Get page via unique identifier:

            https://amsterdam.nl/@{itmidt}/page/?new_json=true&pager_rows=1000      (list of pages)
            https://amsterdam.nl/@{itmidt}/page/?AppIdt=app-pagetype&reload=true    (single page)
    """

    def __init__(self, backend_host='api-server', backend_port=8000, base_path='/api/v1/ingest', headers=dict):
        self.logger = Logger()
        self.backend_host = backend_host
        self.backend_port = backend_port
        self.base_path = base_path
        self.headers = headers
        self.image = Image(backend_host=backend_host, backend_port=backend_port, base_path=base_path, headers=headers)
        self.news = IproxNews(backend_host=backend_host, backend_port=backend_port, base_path=base_path, headers=headers)
        self.paths = {
            'brug': '/projecten/bruggen/maatregelen-vernieuwen-bruggen/',
            'kade': '/projecten/kademuren/maatregelen-vernieuwing/',
            'bouw-en-verkeer': '/projecten/overzicht/'
        }

    def get_images(self, fpd_details):
        # Add image objects to the download queue
        for images in fpd_details['images']:
            for size in images['sources']:
                image_object = images['sources'][size]
                image_object['size'] = size
                self.image.queue.put(image_object)

    def queue_news(self, fpd_details):
        # add news_items to the IproxNews.queue for scraping
        for news_item in fpd_details['news']:
            self.news.queue.put({'news_item': news_item, 'project_type': fpd_details['project_type']})

    def get_set_project_details(self, item, project_type):
        fpd = IproxProject(item['source_url'], item['identifier'])
        fpd.get_data()

        # Skip news items/articles etc...
        if fpd.page_type == 'subhome':
            fpd.parse_data()
            fpd.details['project_type'] = project_type

            # Send data to API-server
            url = 'http://{host}:{port}{base_path}/project'.format(host=self.backend_host,
                                                                   port=self.backend_port,
                                                                   base_path=self.base_path)
            result = requests.post(url, headers=self.headers, json=fpd.details)
            if result.status_code != 200:
                self.logger.error(result.text)
                return None

            # Add images from this project to the download queue
            self.get_images(fpd.details)

            # Add news items from this project to the IproxNews.queue() for fetching
            self.queue_news(fpd.details)

            return fpd.details
        return None

    def get_set_projects(self, project_type):
        # Set the url path from where to fetch the projects
        path = self.paths[project_type]

        # Fetch projects and ingest data
        fpa = IproxProjects(path, project_type)
        fpa.get_data()
        fpa.parse_data()

        url = 'http://{host}:{port}{base_path}/projects'.format(host=self.backend_host,
                                                                port=self.backend_port,
                                                                base_path=self.base_path)

        updated = new = failed = 0
        for item in fpa.parsed_data:
            try:
                existing_project = False
                result = requests.get(url, headers=self.headers, params={'identifier': item.get('identifier')})
                data = json.loads(result.text)
                if data.get('result') is not None:
                    existing_project = True

                result = self.get_set_project_details(item, project_type)
                if result is not None:
                    item['images'] = result['images']
                    item['district_id'] = result['district_id']
                    item['district_name'] = result['district_name']
                    result = requests.post(url, headers=self.headers, json=item)
                    if result.status_code != 200:
                        self.logger.error(result.text)
                        return

                    # Keep track of amount of updates/new insertions
                    if existing_project is True:
                        updated += 1
                    else:
                        new += 1
                else:
                    payload = {'identifier': item.get('identifier')}
                    result = requests.delete(url, headers=self.headers, json=payload)
                    if result.status_code != 200:
                        self.logger.error(result.text)
                    else:
                        self.logger.info('Project {identifier} deleted'.format(identifier=item.get('identifier')))
            except Exception as error:
                self.logger.error('failed ingesting data {project}: {error}'.format(project=item.get('title'),
                                                                                    error=error))
                failed += 1

        # Get images and IproxNews multi-threaded to speed up the scraping-process
        threads = list()

        # Fetch news
        thread_news = threading.Thread(target=self.news.run)
        thread_news.start()
        threads.append(thread_news)

        # Fetch images (queue is filled during project scraping)
        thread_image = threading.Thread(target=self.image.run, kwargs=({'module': 'Iprox Project Details'}))
        thread_image.start()
        threads.append(thread_image)

        # Join threads (blocking!)
        for thread in threads:
            thread.join()

        return {'new': new, 'updated': updated, 'failed': failed, 'project_type': project_type}

    def get_stads_loketten(self):
        # Scrape StadsLoketten
        stads_loketten = IproxStadslokettenScraper(backend_host=self.backend_host,
                                                   backend_port=self.backend_port,
                                                   headers=self.headers)
        stads_loketten.run()
        return {'status': True, 'result': 'scraped stads-loketten'}

    def start(self, project_type):
        result = {}
        if project_type in ['brug', 'kade', 'bouw-en-verkeer']:
            result = self.get_set_projects(project_type)
        elif project_type in ['stadsloket']:
            result = self.get_stads_loketten()
        return print(result)
