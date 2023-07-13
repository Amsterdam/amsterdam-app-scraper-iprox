""" This is the main entry point for the Iprox scraper. It will try to scrape the web-pages from
    amsterdam.nl
"""
import sys
import os
import datetime
from uuid import uuid4
import requests
from FetchData.IproxIngestion import IproxIngestion
from GenericFunctions.AESCipher import AESCipher
from GenericFunctions.IsReachable import IsReachable
from GenericFunctions.Logger import Logger

# Get environment parameters: BACKEND host and port
aes_secret = os.getenv('AES_SECRET')
backend_host = os.getenv('TARGET', 'construction-work')
backend_port = int(os.getenv('TARGET_PORT', '8000'))
base_path = os.getenv('BASE_PATH', '/api/v1/ingest')
garbage_collect = bool(os.getenv('GARBAGE_COLLECT', 'true') == 'true')
logger = Logger()

# Set header
token = AESCipher(str(uuid4()), aes_secret).encrypt()
headers = {'Accept': 'application/json', 'IngestAuthorization': token}


def garbage_collector(project_type, scraper_started):
    """ Start garbage collector on ingestion site

        :param project_type: string
        :param scraper_started: datatime
        :return: scraper_result
    """

    # Setup UserAuthorization Header
    url = 'http://{host}:{port}/api/v1/ingest/garbagecollector'.format(host=backend_host, port=backend_port)
    response = requests.get(
        url,
        headers=headers,
        params={'project_type': project_type, 'date': scraper_started},
        timeout=300
    )

    if response.status_code != 200:
        logger.error(response.text)
        return {}

    # Return scraper result
    data = response.json()
    return data['result']


def main():
    """ Main entry point for the scraper
    """
    # Check if API-server is alive
    if not IsReachable(backend_host=backend_host, backend_port=backend_port).check():
        print('API-server unreachable: Iprox scraper aborted', flush=True)
        sys.exit(1)

    # Set data/time stamp when scraper started, used for garbage collection
    scraper_started = str(datetime.datetime.now())

    # Initialize scraper
    iprox_ingestion = IproxIngestion(
        backend_host=backend_host,
        backend_port=backend_port,
        base_path=base_path,
        headers=headers
    )

    for project_type in ['test_pages', 'stadsloket', 'projects']:
        scraper_report = iprox_ingestion.start(project_type)

        # Call Garbage collector
        if garbage_collect is True:
            scraper_report['garbage_collector'] = garbage_collector(project_type, scraper_started)

        # TO IMPLEMENT...
        # if project_type in ['projects']:
        #     # Send scraper report to backend for processing
        #     print(json.dumps(scraper_report, indent=2))



if __name__ == '__main__':
    # Call the main entry point for the Iprox scraper
    main()
