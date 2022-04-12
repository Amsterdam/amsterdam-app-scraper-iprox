from unittest.mock import patch
from mock_data import TestData
from mock_functions import mocked_requests_get, mocked_requests_post, MockThread
from FetchData.Image import Image as ImageFetcher
from GenericFunctions.Logger import Logger
import requests
import threading


@patch.object(requests, 'get', side_effect=mocked_requests_get)
@patch.object(requests, 'post', side_effect=mocked_requests_post)
@patch.object(threading, 'Thread', side_effect=MockThread)
def test_fetch_image(mocked_requests_get, mocked_requests_post, MockThread):
    image_fetcher = ImageFetcher(headers={'test': 'test_fetch_image'})
    image_fetcher.num_workers = 1
    data = TestData()
    for job in data.image_download_jobs:
        image_fetcher.queue.put(job)

    with patch.object(Logger, 'error', return_value=None) as mock_method:
        image_fetcher.run()
        assert mocked_requests_get.call_count == 1
        assert mocked_requests_post.call_count == 2
        assert image_fetcher.threads[0]['result'] == '\tWorker 0 out of jobs. Images processed: 3'
        mock_method.assert_called_with('Internal server error')
