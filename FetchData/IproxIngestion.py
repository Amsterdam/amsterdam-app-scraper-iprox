""" Iprox ingestion """
import datetime
import json
import requests
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


            https://amsterdam.nl/@337520/page/?AppIdt=app-pagetype&reload=true
    """

    def __init__(self, backend_host='api-server', backend_port=8000, base_path='/api/v1/ingest', headers=dict):
        self.logger = Logger()
        self.backend_host = backend_host
        self.backend_port = backend_port
        self.base_path = base_path
        self.headers = headers
        self.news = IproxNews(backend_host=backend_host,
                              backend_port=backend_port,
                              base_path=base_path,
                              headers=headers)
        self.paths = {'projects': '/projecten/alle-projecten-amsterdam-app'}
        self.scraper_report = {}

    def update_scraper_report(self, data=None, existing_project=False, success=False):
        """ Create report for scraped page """
        project_report = {
            'url': f'https://amsterdam.nl/@{data["identifier"]}/page/',
            'title': data['title'],
            'news': [], 'images': None, 'contacts': None, 'coordinates': None,
            'what': None, 'when': None, 'where': None, 'work': None, 'more-info': None, 'timeline': None,
            'history': 'project is: unreachable/offline'
        }
        if success:
            project_report['news'] = []
            project_report['images'] = len(data['images'])
            project_report['contacts'] = len(data['contacts'])
            project_report['coordinates'] = bool(isinstance(data['coordinates']['lon'], float))
            project_report['what'] = bool(len(data['body']['what']) > 0)
            project_report['when'] = bool(len(data['body']['when']) > 0)
            project_report['where'] = bool(len(data['body']['where']) > 0)
            project_report['work'] = bool(len(data['body']['work']) > 0)
            project_report['more-info'] = bool(len(data['body']['more-info']) > 0)
            project_report['timeline'] = bool(len(data['body']['timeline']) > 0)
            project_report['history'] = 'project is: updated' if existing_project else 'project is: new'

        self.scraper_report[data["identifier"]] = project_report

    def queue_news(self, fpd_details):
        """ add news_items to the IproxNews.queue for scraping """
        for news_item in fpd_details['news']:
            self.news.queue.put({'news_item': news_item, 'project_type': fpd_details['project_type']})

    def get_set_project_details(self, item, project_type):
        """ Get and set project details """
        fpd = IproxProject(item['source_url'], item['identifier'], item['title'])
        fpd.get_data()

        # Skip news items/articles etc...
        if fpd.page_type == 'subhome':
            fpd.parse_data()
            fpd.details['project_type'] = project_type

            # Add news items from this project to the IproxNews.queue() for fetching
            self.queue_news(fpd.details)

            return fpd.details
        return None

    def get_set_projects(self, project_type):
        """ Set the url path from where to fetch the projects """
        path = self.paths[project_type]

        # Fetch projects and ingest data
        fpa = IproxProjects(path, project_type)
        fpa.get_data()
        fpa.parse_data()

        projects_url = f'http://{self.backend_host}:{self.backend_port}{self.base_path}/projects'

        updated = new = failed = deleted = 0
        for item in fpa.parsed_data:
            # DEBUG: Set title for page you'd like to debug...
            # if item['identifier'] != '1145386':
            #     continue
            print('Parsing ', end='')
            print(f'https://amsterdam.nl/@{item["identifier"]}/page/?AppIdt=app-pagetype&reload=true ', end='')
            print(f'title: {item["title"]}', flush=True)
            try:
                result = requests.get(projects_url,
                                      headers=self.headers,
                                      params={'identifier': item.get('identifier')},
                                      timeout=10)
                data = json.loads(result.text)

                existing_project = False
                if data.get('result') is not None:
                    existing_project = True

                fpd_details = self.get_set_project_details(item, project_type)
                if result is not None:
                    # Ingest projects data into construction-work backend
                    item['images'] = fpd_details['images']
                    item['district_id'] = fpd_details['district_id']
                    item['district_name'] = fpd_details['district_name']
                    response = requests.post(projects_url, headers=self.headers, json=item, timeout=10)
                    if response.status_code != 200:
                        self.logger.error(response.text)
                        continue

                    # Ingest project-details data into construction-work backend
                    project_detail_url = f'http://{self.backend_host}:{self.backend_port}{self.base_path}/project'
                    result = requests.post(project_detail_url, headers=self.headers, json=fpd_details, timeout=10)
                    if result.status_code != 200:
                        self.logger.error(result.text)
                        continue

                    # Keep track of amount of updates/new insertions
                    if existing_project is True:
                        updated += 1
                    else:
                        new += 1

                    # update scraper report
                    self.update_scraper_report(data=fpd_details, existing_project=existing_project, success=True)
                else:
                    self.update_scraper_report(data=item, existing_project=existing_project, success=False)
                    payload = {'identifier': item.get('identifier')}
                    result = requests.delete(projects_url, headers=self.headers, json=payload, timeout=10)
                    if result.status_code != 200:
                        self.logger.error(result.text)
                    else:
                        self.logger.info('Project {identifier} deleted'.format(identifier=item.get('identifier')))
                        deleted += 1
            except Exception as error:
                self.logger.error('failed ingesting data {project}: {error}'.format(project=item.get('title'),
                                                                                    error=error))
                failed += 1

        # Fetch news
        print('Fetching news items', flush=True)
        self.news.run(scraper_report=self.scraper_report)

        # Return scraper report
        report = {
            'new': new,
            'updated': updated,
            'failed': failed,
            'deleted': deleted,
            'total': new + updated - deleted,
            'date': str(datetime.datetime.now())
        }
        return report

    def get_stads_loketten(self):
        """ Scrape StadsLoketten """
        stads_loketten = IproxStadslokettenScraper(backend_host=self.backend_host,
                                                   backend_port=self.backend_port,
                                                   headers=self.headers)
        stads_loketten.run()
        return {'status': True, 'result': 'scraped stads-loketten'}

    def start(self, project_type):
        """ First scrape projects, then stads-loketten """
        # report_test_pages = {}
        report_projects = {}
        report_stads_loketten = {}
        # if project_type in ['test_pages']:
        #     report_test_pages = self.get_set_projects(project_type)

        if project_type in ['projects']:
            report_projects = self.get_set_projects(project_type)

        if project_type in ['stadsloket']:
            report_stads_loketten = self.get_stads_loketten()

        return {'projects': report_projects, 'stadsloket': report_stads_loketten}
