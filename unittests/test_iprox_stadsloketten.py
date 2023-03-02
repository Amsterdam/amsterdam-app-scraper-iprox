""" UNITTESTS """
import unittest
from unittest.mock import patch
from unittest import TestCase
import requests
from unittests.mock_functions import mocked_requests_post
from unittests.mock_functions import iprox_stadsloketten_valid
from unittests.mock_functions import iprox_stadsloketten_invalid
from unittests.mock_functions import iprox_stadsloketten_exception
from unittests.mock_functions import iprox_stadsloketten_ingest_fail
from unittests.mock_functions import iprox_stadsloket_valid
from unittests.mock_functions import iprox_stadsloket_invalid
# from unittests.mock_functions import iprox_stadsloket_scraper
from unittests.mock_functions import iprox_stadsloket_exception
# from unittests.mock_functions import iprox_stadsloket_scraper_images
# from unittests.mock_functions import MockThread
from FetchData.IproxStadsloketten import IproxStadsloketten
from FetchData.IproxStadsloketten import IproxStadsloket
# from FetchData.IproxStadsloketten import Scraper


class Unittests(unittest.TestCase):
    """ Unittests """
    @staticmethod
    @patch.object(requests, 'get', side_effect=iprox_stadsloketten_valid)
    @patch.object(requests, 'post', side_effect=mocked_requests_post)
    def test_iprox_stadsloketten_valid(_iprox_stadsloketten_valid, _mocked_requests_post):
        """ Test get stadsloketten """
        isl = IproxStadsloketten(headers={'test': 'test_iprox_stadsloketten_valid'})
        isl.get_data()
        isl.parse_data()

        assert isl.sections == [{'html': 'text', 'text': 'text', 'title': 'contact'}]
        assert isl.stadsloketten == [
            {'title': 'loketten', 'url': 'https://sub-page/', 'identifier': 'acddc71dab316d120cc5d84b5565c874'}
        ]

    @staticmethod
    @patch('requests.get', side_effect=iprox_stadsloketten_invalid)
    def test_iprox_stadsloketten_invalid(_iprox_stadsloketten_invalid):
        """ Test get stadsloketten, invalid result """
        isl = IproxStadsloketten(headers={'test': 'test_iprox_stadsloketten_invalid'})
        isl.get_data()
        isl.parse_data()

        assert not isl.sections
        assert not isl.stadsloketten

    @staticmethod
    @patch('requests.get', side_effect=iprox_stadsloketten_exception)
    def test_iprox_stadsloketten_exception(_iprox_stadsloketten_exception):
        """ Test get stadsloketten, raise exception """
        isl = IproxStadsloketten(headers={'test': 'test_iprox_stadsloketten_exception'})
        isl.get_data()
        isl.parse_data()

        assert not isl.sections
        assert not isl.stadsloketten

    @staticmethod
    @patch('requests.get', side_effect=iprox_stadsloketten_ingest_fail)
    @patch.object(requests, 'post', side_effect=mocked_requests_post)
    def test_iprox_stadsloketten_ingest_fail(_iprox_stadsloketten_ingest_fail, _mocked_requests_post):
        """ Test failed ingestion """
        isl = IproxStadsloketten(headers={'test': 'test_iprox_stadsloketten_ingest_fail'})
        isl.get_data()
        isl.parse_data()

        assert isl.sections == [{'title': 'FAIL INGEST', 'html': 'text', 'text': 'text'}]
        assert isl.stadsloketten == [
            {'title': 'FAIL INGEST', 'url': 'https://sub-page/', 'identifier': 'acddc71dab316d120cc5d84b5565c874'}
        ]

    @staticmethod
    @patch.object(requests, 'post', side_effect=mocked_requests_post)
    @patch('requests.get', side_effect=iprox_stadsloket_valid)
    def test_iprox_stadsloket_valid(_iprox_stadsloket_valid, _mocked_requests_post):
        """ Test valid stadsloketten """
        isl = IproxStadsloket('https://unittest', '0000000000', headers={'test': 'test_iprox_stadsloket_valid'})
        isl.get_data()
        isl.parse_data()

        expected_result = {
            'identifier': '0000000000',
            'contact': {'Openingstijden': {'text': 'text', 'html': 'text'},
                        'Mailen': {'text': 'text', 'html': 'text'}},
            'images': {'type': '', 'sources': {'orig': {'url': 'https://www.amsterdam.nl/1/2/3/test_orig.jpg', 'filename': 'test_orig.jpg', 'image_id': 'c717e41e0e5d4946a62dc567b2fda45e', 'description': ''}, '1px': {'url': 'https://www.amsterdam.nl/1/2/3/1px/text.jpg', 'filename': 'text.jpg', 'image_id': 'c561169ab1afedd2130ee56f89e91a99', 'description': ''}}},  # pylint: disable=line-too-long
            'info': {'html': 'text', 'text': 'text'},
            'title': 'Stadsloket Centrum',
            'address': {'html': 'text', 'text': 'text'}
        }

        TestCase().assertDictEqual(expected_result, isl.details)

    @staticmethod
    @patch.object(requests, 'post', side_effect=mocked_requests_post)
    @patch('requests.get', side_effect=iprox_stadsloket_invalid)
    def test_iprox_stadsloket_invalid(_iprox_stadsloket_invalid, _mocked_requests_post):
        """ Test invalid stadsloketten """
        isl = IproxStadsloket('https://unittest', '0000000000', headers={'test': 'iprox_stadsloket_invalid'})
        isl.get_data()
        isl.parse_data()

        expected_result = {'identifier': '0000000000', 'contact': {}, 'images': {}}

        TestCase().assertDictEqual(expected_result, isl.details)

    @staticmethod
    @patch.object(requests, 'post', side_effect=mocked_requests_post)
    @patch('requests.get', side_effect=iprox_stadsloket_valid)
    def test_iprox_stadsloket_ingest_failed(_iprox_stadsloket_valid, _mocked_requests_post):
        """ Test ingetion stadsloketten failed """
        isl = IproxStadsloket('https://unittest', '0000000000', headers={'test': 'test_iprox_stadsloket_ingest_failed'})
        isl.get_data()
        isl.parse_data()

        expected_result = {
            'identifier': '0000000000',
            'contact': {'Openingstijden': {'text': 'text', 'html': 'text'},
                        'Mailen': {'text': 'text', 'html': 'text'}},
            'images': {'type': '', 'sources': {'orig': {'url': 'https://www.amsterdam.nl/1/2/3/test_orig.jpg', 'filename': 'test_orig.jpg', 'image_id': 'c717e41e0e5d4946a62dc567b2fda45e', 'description': ''}, '1px': {'url': 'https://www.amsterdam.nl/1/2/3/1px/text.jpg', 'filename': 'text.jpg', 'image_id': 'c561169ab1afedd2130ee56f89e91a99', 'description': ''}}},  # pylint: disable=line-too-long
            'info': {'html': 'text', 'text': 'text'},
            'title': 'Stadsloket Centrum',
            'address': {'html': 'text', 'text': 'text'}
        }

        TestCase().assertDictEqual(expected_result, isl.details)

    @staticmethod
    @patch('requests.get', side_effect=iprox_stadsloket_exception)
    def test_ingest_Exception(_iprox_stadsloket_exception):
        """ Test ingestion exception handling """
        isl = IproxStadsloket('https://unittest', '0000000000')
        isl.get_data()
        isl.parse_data()

        expected_result = {'identifier': '0000000000', 'contact': {}, 'images': {}}

        TestCase().assertDictEqual(expected_result, isl.details)

    # Stadsloketten scraper is disabled...

    # @staticmethod
    # @patch('threading.Thread', side_effect=MockThread)
    # @patch('requests.get', side_effect=iprox_stadsloket_scraper)
    # @patch.object(requests, 'post', side_effect=mocked_requests_post)
    # def test_iprox_stads_loket_scraper(_mock_thread, _iprox_stadsloket_scraper, _mocked_requests_post):
    #     """ Test iprox stadsloket scraper """
    #     with patch('FetchData.Image', side_effect=iprox_stadsloket_scraper_images):
    #         scraper = Scraper(headers={'test': 'test_iprox_stads_loket_scraper'})
    #         scraper.run()
    #
    #     assert _mocked_requests_post.call_count == 1
    #     assert _iprox_stadsloket_scraper.call_count == 2
    #     assert _mock_thread.call_count == 0
    #     assert scraper.image.queue.qsize() == 2
