from unittest.mock import patch, call
from unittest import TestCase
from mock_data import TestData
from FetchData.IproxProjects import IproxProjects
from GenericFunctions.Logger import Logger
from mock_functions import mocked_requests_get

expected_raw_data = [{'category': 'Mock', 'feedid': 'https://mock/', 'publication_date': '1970-01-01', 'modification_date': '1970-01-01', 'image_url': 'https://mock', 'title': 'mock: data', 'content': '<div><p>mock</p></div>', 'source_url': 'https://mock', 'related_articles': '', 'author': '', 'photo_author': '', 'images': []}]
iprox_parsed_data = [{'project_type': 'identifier', 'identifier': '0defd864f86f6d3110a0fca7fa403991', 'district_id': -1, 'district_name': '', 'title': 'mock', 'subtitle': 'Data', 'content_html': '<div><p>mock</p></div>', 'content_text': 'mock', 'images': [], 'publication_date': '1970-01-01', 'modification_date': '1970-01-01', 'source_url': 'https://mock'}]


@patch.object(Logger, 'error')
@patch('requests.get', mocked_requests_get)
def test_get_data_raise_exception(mock):
    iprox_project = IproxProjects('/raise_exception', 'identifier')
    iprox_project.get_data()

    assert mock.call_args_list == [call('failed fetching data from https://www.amsterdam.nl/raise_exception?new_json=true&pager_rows=1000: Mock exception')]


@patch.object(Logger, 'error')
@patch('requests.get', mocked_requests_get)
def test_get_data(mock):
    iprox_project = IproxProjects('/get', 'identifier')
    iprox_project.get_data()

    TestCase().assertListEqual(iprox_project.raw_data, expected_raw_data)


def test_parse_data():
    test_data = TestData()
    iprox_project = IproxProjects('/get', 'identifier')
    iprox_project.raw_data = test_data.iprox_projects
    iprox_project.parse_data()

    TestCase().assertListEqual(iprox_project.parsed_data, iprox_parsed_data)


@patch.object(Logger, 'error')
def test_parse_data_raise_exception(mock):
    test_data = TestData()
    test_data.iprox_projects[0]['title'] = b'0xFFFF'  # Bytes are not str.splittable
    iprox_project = IproxProjects('/get', 'identifier')
    iprox_project.raw_data = test_data.iprox_projects
    iprox_project.parse_data()

    assert mock.call_args_list == [call("failed parsing data from https://www.amsterdam.nl/get?new_json=true&pager_rows=1000: a bytes-like object is required, not 'str'")]
