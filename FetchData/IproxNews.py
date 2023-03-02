""" Fetch news articles from the Iprox system """
import base64
from queue import Queue
import requests
from GenericFunctions.Hashing import Hashing
from GenericFunctions.Logger import Logger
from GenericFunctions.TextSanitizers import TextSanitizers
from FetchData.Image import Image
from FetchData.IproxRecursion import IproxRecursion


class IproxNews:
    """ Fetch news items from Iprox. News items feeds are read from a queue and processed

        a queued news item looks like:

        {'identifier': md5hash, 'source_identifier': md5hash, 'url': string}
    """

    def __init__(self, backend_host='api-server', backend_port=8000, base_path='/api/v1/ingest', headers=dict):
        self.logger = Logger()
        self.backend_host = backend_host
        self.backend_port = backend_port
        self.base_path = base_path
        self.headers = headers
        self.image = Image(backend_host=backend_host,
                           backend_port=backend_port,
                           base_path=self.base_path,
                           headers=headers)
        self.sanitizer = TextSanitizers()
        self.hash = Hashing()
        self.queue = Queue()
        self.query_param = '?AppIdt=app-pagetype&reload=true'
        self.page_targets = ['Meta', 'Gegevens', 'Inhoud', 'Verwijzing', 'Download']

    @staticmethod
    def skeleton():
        """ return skeleton dict """
        return {
            'identifier': '',
            'project_identifier': '',
            'url': '',
            'title': '',
            'publication_date': '',
            'body': {
                'summary': {'html': '', 'text': ''},
                'preface': {'html': '', 'text': ''},
                'content': {'html': '', 'text': ''}
            },
            'images': [
                # { EXAMPLE:
                #     'type': 'banner/additional',
                #     'sources': {
                #         'orig': {'url': '', 'image_id': '', 'filename': '', 'description': ''},
                #         '80px': {'url': '', 'image_id': '', 'filename': '', 'description': ''},
                #         '220px': {'url': '', 'image_id': '', 'filename': '', 'description': ''},
                #         '460px': {'url': '', 'image_id': '', 'filename': '', 'description': ''},
                #         '700px': {'url': '', 'image_id': '', 'filename': '', 'description': ''}
                #     }
                # }
            ],
            'assets': [
                # { EXAMPLE:
                #     'identifier': md5hash,
                #     'mime_type': 'application/pdf',
                #     'url': string,
                #     'title': string,
                #     'filename': string,
                #     'data': binary data
                # }
            ]
        }

    def get_data(self, url):
        """
        request data from data-end point

        :return: json or None
        """
        try:
            result = requests.get(url, timeout=10)
            return result.json()
        except Exception as error:
            self.logger.error('failed fetching data from {url}: {error}'.format(url=url, error=error))
        return None

    def get_set_asset(self, identifier, mime_type, url):
        """ Downloads assets from Iprox server (pdf, images) """

        # Check if we already have this asset on API Server, Prevent API-bandwidth saturation
        url = f'http://{self.backend_host}:{self.backend_port}{self.base_path}/asset'
        result_api_server_get = requests.get(url,
                                             headers=self.headers,
                                             params={'identifier': identifier},
                                             timeout=10).json()
        if result_api_server_get['status'] is False:
            asset_result = requests.get(url, timeout=10)
            if asset_result.status_code == 200:
                payload = {
                    'identifier': identifier,
                    'url': url,
                    'mime_type': mime_type,
                    'data': base64.b64encode(asset_result.content)
                }
                result_api_server_post = requests.post(url, headers=self.headers, json=payload, timeout=10)
                if result_api_server_post.status_code != 200:
                    self.logger.error(result_api_server_post.text)

    def filter_results(self, data):
        """ Get filtered results from the iprox system """
        iprox = IproxRecursion()
        return iprox.filter(data, [], targets=self.page_targets)

    def scraper(self, news_item):
        """ Actual scraper logic, create object, scrape data, populate object, save """
        raw_data = self.get_data(news_item.get('url'))
        if raw_data is None or raw_data == {}:
            return {}

        news_item_data = self.skeleton()

        page = raw_data.get('item', {}).get('page', {})
        date = page.get('CorDtm')

        news_item_data['publication_date'] = '{year}-{month}-{day}'.format(year=date[0:4],
                                                                           month=date[4:6],
                                                                           day=date[6:8])

        news_item_data['identifier'] = news_item.get('identifier')
        news_item_data['project_identifier'] = news_item.get('project_identifier')
        news_item_data['url'] = news_item.get('url')
        news_item_data['title'] = page.get('title', '')

        filtered_results = self.filter_results(page.get('cluster', []))

        for i in range(0, len(filtered_results), 1):  # pylint: disable=too-many-nested-blocks
            if filtered_results[i].get('Gegevens', None) is not None:
                for j in range(0, len(filtered_results[i]['Gegevens']), 1):
                    # Get summary for this news item
                    if filtered_results[i]['Gegevens'][j].get('Nam') == 'Samenvatting':
                        html = filtered_results[i]['Gegevens'][j].get('Txt')
                        news_item_data['body']['summary']['text'] = self.sanitizer.strip_html(html)
                        news_item_data['body']['summary']['html'] = self.sanitizer.rewrite_html(html)

                    if filtered_results[i]['Gegevens'][j].get('Nam') == 'Brondatum':
                        date = filtered_results[i]['Gegevens'][j].get('Dtm', '')
                        news_item_data['publication_date'] = '{year}-{month}-{day}'.format(year=date[0:4],
                                                                                           month=date[4:6],
                                                                                           day=date[6:8])

                    # Get main image for news item
                    if filtered_results[i]['Gegevens'][j].get('Nam') == 'Hero afbeelding':
                        data = filtered_results[i]['Gegevens'][j]
                        domain = 'https://www.amsterdam.nl'
                        location = data.get('Src', {}).get('_', '')
                        image = {
                            'type': 'banner',
                            'sources': {
                                'orig': {
                                    'url': '{domain}{location}'.format(domain=domain, location=location),
                                    'image_id': self.hash.make_md5_hash('{domain}{location}'.format(domain=domain,
                                                                                                    location=location)),
                                    'filename': data.get('FilNam', ''),
                                    'description': ''}
                            }
                        }
                        for asset in data.get('asset'):
                            location = asset.get('Src', {}).get('_')
                            filename = asset.get('FilNam', '')
                            size = location.split('/')[-2]
                            image['sources'][size] = {
                                'url': '{domain}{location}'.format(domain=domain, location=location),
                                'image_id': Hashing().make_md5_hash('{domain}{location}'.format(domain=domain,
                                                                                                location=location)),
                                'filename': filename,
                                'description': ''
                            }
                        news_item_data['images'].append(image)

            if filtered_results[i].get('Inhoud', None) is not None:
                for j in range(0, len(filtered_results[i]['Inhoud']), 1):
                    # Get preface for this news item
                    if filtered_results[i]['Inhoud'][j].get('Nam') == 'Inleiding':
                        html = filtered_results[i]['Inhoud'][j].get('Txt')
                        news_item_data['body']['preface']['text'] = self.sanitizer.strip_html(html)
                        news_item_data['body']['preface']['html'] = self.sanitizer.rewrite_html(html)

                    # Get content for this news item
                    if filtered_results[i]['Inhoud'][j].get('Nam') == 'Tekst':
                        html = filtered_results[i]['Inhoud'][j].get('Txt')
                        news_item_data['body']['content']['text'] = self.sanitizer.strip_html(html)
                        news_item_data['body']['content']['html'] = self.sanitizer.rewrite_html(html)

                        # Get additional images for this news item
                        for asset in filtered_results[i]['Inhoud'][j].get('asset', {}):
                            if isinstance(asset, str):
                                asset = filtered_results[i]['Inhoud'][j]['asset']
                            domain = 'https://www.amsterdam.nl'
                            location = asset.get('Src', '')
                            size = location.split('/')[-2]
                            image = {
                                'type': 'additional',
                                'sources': {
                                    size: {
                                        'url': '{domain}/publish/{location}'.format(domain=domain, location=location),
                                        'image_id': self.hash.make_md5_hash(f'{domain}{location}'),
                                        'filename': location.split('/')[-1],
                                        'description': ''}
                                }
                            }
                            news_item_data['images'].append(image)

            # Get assets for this news item
            if filtered_results[i].get('Verwijzing', None) is not None:
                if filtered_results[i]['Verwijzing'].get('veld', {}).get('Nam') == 'Bestand':
                    source = filtered_results[i]['Verwijzing']['veld']
                    url = 'https://www.amsterdam.nl{source}'.format(source=source.get('Src', {}).get('_'))
                    identifier = self.hash.make_md5_hash(url)
                    mime_type = 'application/{mime_type}'.format(mime_type=source.get('FilNam', '').split('.')[-1])

                    self.get_set_asset(identifier, mime_type, url)
                    news_item_data['assets'].append({
                        'identifier': identifier,
                        'mime_type': mime_type,
                        'url': url,
                        'title': source.get('Wrd', ''),
                        'filename': source.get('FilNam', '')
                    })

        return news_item_data

    def save_news_item(self, news_item_data):
        """ Post data to backend server """
        url = f'http://{self.backend_host}:{self.backend_port}{self.base_path}/news'
        result = requests.post(url, headers=self.headers, json=news_item_data, timeout=10)
        if result.status_code != 200:
            self.logger.error(result.text)

    def get_images(self, news_item_data):
        """ Add image objects to the download queue """
        if 'images' in news_item_data:
            for images in news_item_data['images']:
                for size in images['sources']:
                    image_object = images['sources'][size]
                    image_object['size'] = size
                    self.image.queue.put(image_object)
        else:
            print('No images for news item')

    def run(self):
        """ Keep getting jobs from a queue until the queue is empty. Scrape each item from the queue """
        while not self.queue.empty():
            # Get queued news_items and scrape data
            job = self.queue.get()
            news_item_data = self.scraper(job['news_item'])
            print(f'Parsing News: {job["news_item"]["url"]}', flush=True)

            if news_item_data is not None:
                news_item_data['project_type'] = job['project_type']
                self.save_news_item(news_item_data)
                self.get_images(news_item_data)

        # Download images for each scraped news item
        self.image.run(module='Iprox News items')
