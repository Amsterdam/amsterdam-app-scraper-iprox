""" Mock functions """
import threading
from queue import Queue
from unittests.mock_data import TestData


def mocked_socket_connect_ok(*args):
    """ Mock socket connect ok """
    return


def mocked_socket_connect_fail(*args):
    """ Mock socket connect raise exception """
    raise Exception('Connection error')  # pylint: disable=broad-exception-raised


def mocked_requests_post(*args, **kwargs):
    """ Mock post request """
    class MockResponse:
        """ Mock response """
        def __init__(self, status_code, text=None, json_data=None):
            self.status_code = status_code
            self.binary_data = [b'0', b'1']
            self.json_data = json_data
            self.text = text

        def iter_content(self, size):
            """ Mocker iter """
            for data in self.binary_data:
                yield data

        def json(self):
            """ Mock json """
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
    """ Mock request """
    class MockResponse:
        """ Mock response """
        def __init__(self, status_code, json_data=None):
            self.status_code = status_code
            self.binary_data = [b'0', b'1']
            self.json_data = json_data

        def iter_content(self, size):
            """ Mock iter """
            for data in self.binary_data:
                yield data

        def json(self):
            """ Mock json """
            return self.json_data

    if args[0] == 'http://api-server:8000/api/v1/ingest/image':
        return MockResponse(200, json_data={'status': False, 'result': None})

    if args[0] == 'valid_url':
        return MockResponse(200)

    if args[0] == 'invalid_url':
        return MockResponse(404)

    if args[0] == 'empty_json_response?AppIdt=app-pagetype&reload=true':
        return MockResponse(200, json_data={})

    if args[0] == 'valid_json_response?AppIdt=app-pagetype&reload=true':
        return MockResponse(200, json_data={'item': {'page': {'pagetype': 'mock'}}})

    if args[0] == 'raise_exception?AppIdt=app-pagetype&reload=true':
        raise Exception('Mock exception')  # pylint: disable=broad-exception-raised

    if args[0] == 'https://www.amsterdam.nl/raise_exception?new_json=true&pager_rows=1000':
        raise Exception('Mock exception')  # pylint: disable=broad-exception-raised

    if args[0] == 'https://www.amsterdam.nl/get?new_json=true&pager_rows=1000':
        test_data = TestData()
        return MockResponse(200, json_data=test_data.iprox_projects)

    if args[0] == 'https://mock_nieuws/?new_json=true':
        test_data = TestData()
        return MockResponse(200, json_data=test_data.news_data)

    if args[0] == 'https://amsterdam.nl/@000000-news/page/?AppIdt=app-pagetype&reload=true':
        test_data = TestData()
        return MockResponse(200, json_data=test_data.news_data)

    if args[0] == 'https://mock-timeline?AppIdt=app-pagetype&reload=true':
        test_data = TestData()
        return MockResponse(200, json_data=test_data.timeline_raw)


class MockThread(threading.Thread):
    """ Mock threads """
    def __init__(self, target=None, args=None, kwargs=None):
        super(MockThread, self).__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def start(self):
        """ Mock start """
        if self.args is not None:
            self.target(*self.args)
        else:
            self.target(**self.kwargs)

    def run(self):
        """ Once a thread object is created, its activity must be started by calling the thread's start() method.
            This invokes the run() method in a separate thread of control.
        """
        return

    @staticmethod
    def join(*args, **kwargs):
        """ Mock join """
        return


def iprox_stadsloketten_valid(*args, **kwargs):
    """ Mock request """
    class Response:
        """ Mock response """
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            """ Mock json """
            return self.test_data.iprox_stadsloketten
    return Response()


def iprox_stadsloketten_invalid(*args, **kwargs):
    """ Mock request """
    class Response:
        """ Mock response """
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            """ Mock json """
            return {}
    return Response()


def iprox_stadsloketten_exception(*args, **kwargs):
    """ Mock request """
    class Response:
        """ Mock response """
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            """ Mock json """
            return 'Exception Data'
    return Response()


def iprox_stadsloketten_ingest_fail(*args, **kwargs):
    """ Mock request """
    class Response:
        """ Mock reponse """
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            """ Mock json """
            return self.test_data.iprox_stadsloketten_ingest_fail
    return Response()


def iprox_stadsloket_valid(*args, **kwargs):
    """ Mock request """
    class Response:
        """ Mock response """
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            """ Mock json """
            return self.test_data.iprox_stadsloket
    return Response()


def iprox_stadsloket_invalid(*args, **kwargs):
    """ Mock request """
    class Response:
        """ Mock response """
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            """ Mock json """
            return {}
    return Response()


def iprox_stadsloket_exception(*args, **kwargs):
    """ Mock request """
    class Response:
        """ Mock response """
        def __init__(self, *args, **kwargs):
            self.test_data = TestData()

        def json(self):
            """ Mock json """
            return 'Exception Data'
    return Response()


def iprox_stadsloket_scraper(url, **kwargs):
    """ Mock request """
    class Response:
        """ Mock response """
        def __init__(self, url, **kwargs):
            self.url = url
            self.test_data = TestData()

        def json(self):
            """ Mock json """
            if self.url == 'https://www.amsterdam.nl/contact/?AppIdt=app-pagetype&reload=true':
                return self.test_data.iprox_stadsloketten
            return self.test_data.iprox_stadsloket
    return Response(url, **kwargs)


def iprox_stadsloket_scraper_images(*args, **kwargs):
    """ Mock scraper """
    class Scraper:
        """ Mock scraper"""
        def __init__(self, *args, **kwargs):
            self.queue = Queue()
    return Scraper()


def iprox_filter(*args, **kwargs):
    """ Mock filter """
    mock_data = TestData()
    return mock_data.iprox_project_detail
