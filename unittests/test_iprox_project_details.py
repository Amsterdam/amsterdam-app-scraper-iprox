""" UNITTESTS """
import unittest
from unittest.mock import patch, call
from unittest import TestCase
from unittests.mock_data import TestData
from unittests.mock_functions import mocked_requests_get, iprox_filter
from FetchData.IproxProject import IproxProject
from FetchData.IproxRecursion import IproxRecursion
from GenericFunctions.Logger import Logger


class Unittests(unittest.TestCase):
    """ Unittests """
    @staticmethod
    @patch('requests.get', mocked_requests_get)
    def test_get_data_valid_item_is_none():
        """ Test get empty page """
        iprox_project = IproxProject('empty_json_response', 'identifier', 'title')
        iprox_project.get_data()

        assert iprox_project.identifier == 'identifier'
        assert iprox_project.page == {}
        assert iprox_project.page_type == ''
        assert iprox_project.url == 'empty_json_response?AppIdt=app-pagetype&reload=true'

    @staticmethod
    @patch('requests.get', mocked_requests_get)
    def test_get_data_valid_item_is_not_none():
        """ Test get valid page """
        iprox_project = IproxProject('valid_json_response', 'identifier', 'title')
        iprox_project.get_data()

        assert iprox_project.identifier == 'identifier'
        assert iprox_project.page == {'pagetype': 'mock'}
        assert iprox_project.page_type == 'mock'
        assert iprox_project.url == 'valid_json_response?AppIdt=app-pagetype&reload=true'

    @staticmethod
    @patch.object(Logger, 'error')
    @patch('requests.get', mocked_requests_get)
    def test_get_data_raise_exception(mock):
        """ Test get data with raised exception """
        iprox_project = IproxProject('raise_exception', 'identifier', 'title')
        iprox_project.get_data()

        assert iprox_project.identifier == 'identifier'
        assert iprox_project.page == {}
        assert iprox_project.page_type == ''
        assert iprox_project.url == 'raise_exception?AppIdt=app-pagetype&reload=true'
        assert mock.call_args_list == [call('failed fetching data from raise_exception?AppIdt=app-pagetype&reload=true: Mock exception')]  # pylint: disable=line-too-long

    @staticmethod
    @patch('requests.get', mocked_requests_get)
    @patch.object(IproxRecursion, 'filter', side_effect=iprox_filter)
    def test_parse_data(_iprox_filter):
        """ Test parse data """
        test_data = TestData()
        iprox_project = IproxProject('None', 'identifier', '')
        iprox_project.page = {'pagetype': 'subhome'}
        iprox_project.raw_data = {'item': {'Url': 'https://mock/mock/mock/', 'relUrl': 'mock/mock'}}
        iprox_project.parse_data()

        TestCase().assertDictEqual(iprox_project.details, test_data.iprox_project_details)

    @staticmethod
    @patch('requests.get', mocked_requests_get)
    def test_get_timeline():
        """ Test get timeline """
        iprox_project = IproxProject('None', 'identifier', 'title')
        iprox_project.get_timeline('https://mock-timeline')

        expected_result = {
            'title': {'text': 'mock', 'html': '<div>mock</div>'},
            'intro': {'text': 'mock', 'html': '<div>mock</div>'},
            'items': [
                {'content': [],
                 'title': 'mock', 'progress': '', 'collapsed': True}
            ]
        }

        TestCase().assertDictEqual(iprox_project.details['body']['timeline'], expected_result)
