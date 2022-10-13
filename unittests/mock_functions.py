import json
import threading
from mock_data import TestData
from queue import Queue


def mocked_socket_connect_ok(*args):
    pass


def mocked_socket_connect_fail(*args):
    raise Exception('Connection error')


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, text=None, json_data=None):
            self.status_code = status_code
            self.binary_data = [b'0', b'1']
            self.json_data = json_data
            self.text = text

        def iter_content(self, size):
            for data in self.binary_data:
                yield data

        def json(self):
            return self.json_data

    if kwargs['headers']['test'] == 'test_fetch_image':
        data = kwargs['json']
        if data.get('filename', None) == 'mock0.jpg':
            return MockResponse(200, json_data={'status': True, 'result': True})
        if data.get('filename', None) == 'fail_saving.jpg':
            return MockResponse(500, text='Internal server error')

    if kwargs['headers']['test'] == 'test_iprox_stadsloket_valid':
        return MockResponse(200, json_data={'status': True, 'result': True})

    if kwargs['headers']['test'] == 'test_iprox_stadsloket_ingest_failed':
        return MockResponse(500, json_data={'status': False, 'result': False})

    if kwargs['headers']['test'] == 'test_iprox_stadsloketten_ingest_fail':
        return MockResponse(500, json_data={'status': False, 'result': False})

    if kwargs['headers']['test'] == 'test_iprox_stadsloketten_valid':
        return MockResponse(200, json_data={'status': True, 'result': True})

    if kwargs['headers']['test'] == 'test_iprox_stads_loket_scraper':
        return MockResponse(200, json_data={'status': True, 'result': True})


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, json_data=None):
            self.status_code = status_code
            self.binary_data = [b'0', b'1']
            self.json_data = json_data

        def iter_content(self, size):
            for data in self.binary_data:
                yield data

        def json(self):
            return self.json_data

    if args[0] == 'http://api-server:8000/api/v1/ingest/image':
        return MockResponse(200, json_data={'status': False, 'result': None})
    elif args[0] == 'valid_url':
        return MockResponse(200)
    elif args[0] == 'invalid_url':
        return MockResponse(404)
    elif args[0] == 'empty_json_response?AppIdt=app-pagetype&reload=true':
        return MockResponse(200, json_data={})
    elif args[0] == 'valid_json_response?AppIdt=app-pagetype&reload=true':
        return MockResponse(200, json_data={'item': {'page': {'pagetype': 'mock'}}})
    elif args[0] == 'raise_exception?AppIdt=app-pagetype&reload=true':
        raise Exception('Mock exception')
    elif args[0] == 'https://www.amsterdam.nl/raise_exception?new_json=true&pager_rows=1000':
        raise Exception('Mock exception')
    elif args[0] == 'https://www.amsterdam.nl/get?new_json=true&pager_rows=1000':
        test_data = TestData()
        return MockResponse(200, json_data=test_data.iprox_projects)
    elif args[0] == 'https://mock_nieuws/?new_json=true':
        test_data = TestData()
        return MockResponse(200, json_data=test_data.news_data)
    elif args[0] == 'https://amsterdam.nl/@000000-news/page/?AppIdt=app-pagetype&reload=true':
        test_data = TestData()
        return MockResponse(200, json_data=test_data.news_data)
    elif args[0] == 'https://mock-timeline?AppIdt=app-pagetype&reload=true':
        test_data = TestData()
        return MockResponse(200, json_data=test_data.timeline_raw)


class MockThread(threading.Thread):
    def __init__(self, target=None, args=None, kwargs=None):
        super(MockThread, self).__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def start(self):
        if self.args is not None:
            self.target(*self.args)
        else:
            self.target(**self.kwargs)

    def run(self):
        """ Once a thread object is created, its activity must be started by calling the thread's start() method.
            This invokes the run() method in a separate thread of control.
        """
        pass

    @staticmethod
    def join(**kwargs):
        return


def iprox_stadsloketten_valid(*args, **kwargs):
    class Response:
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            return self.test_data.iprox_stadsloketten
    return Response()


def iprox_stadsloketten_invalid(*args, **kwargs):
    class Response:
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            return {}
    return Response()


def iprox_stadsloketten_exception(*args, **kwargs):
    class Response:
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            return 'Exception Data'
    return Response()


def iprox_stadsloketten_ingest_fail(*args, **kwargs):
    class Response:
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            return self.test_data.iprox_stadsloketten_ingest_fail
    return Response()


def iprox_stadsloket_valid(*args, **kwargs):
    class Response:
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            return self.test_data.iprox_stadsloket
    return Response()


def iprox_stadsloket_invalid(*args, **kwargs):
    class Response:
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            return {}
    return Response()


def iprox_stadsloket_exception(*args, **kwargs):
    class Response:
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            return 'Exception Data'
    return Response()


def iprox_stadsloket_scraper(url, **kwargs):
    class Response:
        def __init__(self, url, **kwargs):
            self.url = url
            self.test_data = TestData()

        def json(self):
            if self.url == 'https://www.amsterdam.nl/contact/?AppIdt=app-pagetype&reload=true':
                return self.test_data.iprox_stadsloketten
            else:
                return self.test_data.iprox_stadsloket
    return Response(url, **kwargs)


def iprox_stadsloket_scraper_images(*args, **kwargs):
    class Scraper:
        def __init__(self, *args, **kwargs):
            self.queue = Queue()
    return Scraper()


def iprox_filter(*args, **kwargs):
    mock_data = TestData()
    return mock_data.iprox_project_detail
