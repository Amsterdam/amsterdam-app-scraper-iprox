import base64
import json
import re
import requests
import datetime
from queue import Queue
from GenericFunctions.Logger import Logger
from GenericFunctions.TextSanitizers import TextSanitizers
from FetchData.Image import Image
from FetchData.IproxRecursion import IproxRecursion
from GenericFunctions.Hashing import Hashing
# from models import Assets, News


class IproxNews:
    """ Fetch news items from Iprox. News items feeds are read from a queue and processed

        a queued news item looks like:

        {'identifier': md5hash, 'source_identifier': md5hash, 'url': string}
    """

    def __init__(self, backend_host='api-server', backend_port=8000, headers=dict):
        self.logger = Logger()
        self.backend_host = backend_host
        self.backend_port = backend_port
        self.headers = headers
        self.image = Image(backend_host=backend_host, backend_port=backend_port, headers=headers)
        self.sanitizer = TextSanitizers()
        self.hash = Hashing()
        self.queue = Queue()
        self.query_param = '?AppIdt=app-pagetype&reload=true'
        self.page_targets = ['Meta', 'Gegevens', 'Inhoud', 'Verwijzing', 'Download']

    @staticmethod
    def skeleton():
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
            result = requests.get('{url}{query_param}'.format(url=url, query_param=self.query_param))
            return result.json()
        except Exception as error:
            self.logger.error('failed fetching data from {url}: {error}'.format(url=url, error=error))
        return None

    def get_set_asset(self, identifier, mime_type, url):
        # Check if we already have this asset on API Server, Prevent API-bandwidth saturation
        url = 'http://{host}:{port}/api/v1/ingest/asset'.format(host=self.backend_host, port=self.backend_port)
        result_api_server_get = requests.get(url, headers=self.headers, params={'identifier': identifier}).json()
        if result_api_server_get['status'] is False:
            asset_result = requests.get(url)
            if asset_result.status_code == 200:
                payload = {
                    'identifier': identifier,
                    'url': url,
                    'mime_type': mime_type,
                    'data': base64.b64encode(asset_result.content)
                }
                result_api_server_post = requests.post(url, headers=self.headers, json=json.dumps(payload))
                if result_api_server_post.status_code != 200:
                    self.logger.error(result_api_server_post.text)

    def filter_results(self, data):
        iprox = IproxRecursion()
        return iprox.filter(data, [], targets=self.page_targets)

    def scraper(self, news_item):
        raw_data = self.get_data(news_item.get('url'))
        if raw_data is None:
            return

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

        for i in range(0, len(filtered_results), 1):
            if filtered_results[i].get('Gegevens', None) is not None:
                for j in range(0, len(filtered_results[i]['Gegevens']), 1):
                    # Get summary for this news item
                    if filtered_results[i]['Gegevens'][j].get('Nam') == 'Samenvatting':
                        news_item_data['body']['summary']['text'] = self.sanitizer.strip_html(filtered_results[i]['Gegevens'][j].get('Txt'))
                        html = filtered_results[i]['Gegevens'][j].get('Txt')
                        news_item_data['body']['summary']['html'] = re.sub('/publish/pages/', 'https://www.amsterdam.nl/publish/pages/', html)

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
                        news_item_data['body']['preface']['text'] = self.sanitizer.strip_html(filtered_results[i]['Inhoud'][j].get('Txt'))
                        html = filtered_results[i]['Inhoud'][j].get('Txt')
                        news_item_data['body']['preface']['html'] = re.sub('/publish/pages/', 'https://www.amsterdam.nl/publish/pages/', html)

                    # Get content for this news item
                    if filtered_results[i]['Inhoud'][j].get('Nam') == 'Tekst':
                        news_item_data['body']['content']['text'] = self.sanitizer.strip_html(filtered_results[i]['Inhoud'][j].get('Txt'))
                        html = filtered_results[i]['Inhoud'][j].get('Txt')
                        news_item_data['body']['content']['html'] = re.sub('/publish/pages/', 'https://www.amsterdam.nl/publish/pages/', html)

                        # Get additional images for this news item
                        for asset in filtered_results[i]['Inhoud'][j].get('asset', {}):
                            domain = 'https://www.amsterdam.nl'
                            location = asset.get('Src', '')
                            size = location.split('/')[-2]
                            image = {
                                'type': 'additional',
                                'sources': {
                                    size: {
                                        'url': '{domain}/publish/{location}'.format(domain=domain, location=location),
                                        'image_id': self.hash.make_md5_hash('{domain}{location}'.format(domain=domain,
                                                                                                        location=location)),
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
        url = 'http://{host}:{port}/api/v1/ingest/news'.format(host=self.backend_host, port=self.backend_port)
        result = requests.post(url, headers=self.headers, json=json.dumps(news_item_data))
        if result.status_code != 200:
            self.logger.error(result.text)

    def get_images(self, news_item_data):
        # Add image objects to the download queue
        for images in news_item_data['images']:
            for size in images['sources']:
                image_object = images['sources'][size]
                image_object['size'] = size
                self.image.queue.put(image_object)

    def run(self):
        while not self.queue.empty():
            # Get queued news_items and scrape data
            job = self.queue.get()
            news_item_data = self.scraper(job['news_item'])
            news_item_data['project_type'] = job['project_type']
            self.save_news_item(news_item_data)
            self.get_images(news_item_data)
        else:
            # Download images for each scraped news item
            self.image.run(module='Iprox News items')
