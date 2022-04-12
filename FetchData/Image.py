import base64
import json
import time
import requests
import threading
from queue import Queue
from GenericFunctions.Logger import Logger


class Image:
    """ This class is a multi-threaded image fetcher. It has a queue from which workers (threads) fetch a job.

        A job looks like:
        {
            'url': 'https://.../some-image.jpg',
            'image_id': '1ffff06a468ae9a566ca11951faa1ce3',
            'filename': 'some-image.jpg',
            'description': '',
            'size': 'orig'
        }

        Once the worker has the image retrieved from the url, it will set the mime-type, change image_id to identifier
        and save the result to the database.
    """

    def __init__(self, backend_host='api-server', backend_port=8000, headers=dict):
        self.logger = Logger()
        self.host = backend_host
        self.port = backend_port
        self.headers = headers
        self.num_workers = 10
        self.queue = Queue()
        self.threads = dict()

    def fetch(self, url):
        try:
            # Request image as a stream
            result = requests.get(url, stream=True)
            if result.status_code != 200:
                raise Exception('Failed downloading image: {url}'.format(url=url))

            # start reading from the stream in chunks of 1024 bytes and append to data
            data = b''
            for chunk in result.iter_content(1024):
                data += chunk
            return data
        except Exception as error:
            self.logger.error('failed fetching image data for {url}: {error}'.format(url=url, error=error))
            return None

    def save_image(self, item):
        extension = item['filename'].split('.')[-1]
        item['mime_type'] = 'image/{extension}'.format(extension=extension)
        url = 'http://{host}:{port}/api/v1/ingest/image'.format(host=self.host, port=self.port)
        result = requests.post(url, headers=self.headers, json=item)
        if result.status_code != 200:
            self.logger.error(result.text)

    def worker(self, worker_id):
        count = 0
        while not self.queue.empty():
            item = self.queue.get_nowait()

            # Images use identifier not image_id from other models
            item['identifier'] = item.pop('image_id')

            # Check if we already have this image on API Server, Prevent API-bandwidth saturation
            url = 'http://{host}:{port}/api/v1/ingest/image'.format(host=self.host, port=self.port)
            result = requests.get(url, headers=self.headers, params={'identifier': item['identifier']}).json()

            if result['status'] is False:
                image_data = self.fetch(item['url'])
                if image_data is not None:
                    item['data'] = base64.b64encode(image_data).decode('utf-8')
                    self.save_image(item)
            count += 1
        else:
            self.threads[worker_id]['result'] = '\tWorker {worker_id} out of jobs. Images processed: {count}'.format(worker_id=worker_id, count=count)

    def run(self, module='Undefined'):
        now = time.time()
        self.logger.info('Processing {num} images for {module}'.format(num=self.queue.qsize(), module=module))

        # Start worker threads
        for i in range(0, self.num_workers, 1):
            thread = threading.Thread(target=self.worker, args=(i,))
            self.threads[i] = {'thread': thread, 'result': ''}
            thread.start()

        # Stop worker threads
        for key in self.threads:
            self.threads[key]['thread'].join()
            self.logger.info(self.threads[key]['result'])

        self.logger.info('Processing done in {elapsed:.2f} seconds'.format(elapsed=time.time() - now))
