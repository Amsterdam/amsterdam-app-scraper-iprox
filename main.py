""" This is the main entry point for the Iprox scraper. It will try to scrape the web-pages from
    amsterdam.nl
"""
import sys
import os
from uuid import uuid4
import requests
from FetchData.IproxIngestion import IproxIngestion
from GenericFunctions.AESCipher import AESCipher
from GenericFunctions.IsReachable import IsReachable
from GenericFunctions.Logger import Logger


def main():
    """ Main entry point for the scraper
    """
    # Setup logger
    logger = Logger()

    # Get environment parameters: BACKEND host and port
    backend_host = os.getenv('TARGET', 'api-server')
    backend_port = int(os.getenv('TARGET_PORT', '8000'))
    garbage_collect = bool(os.getenv('GARBAGE_COLLECT', 'true') == 'true')
    base_path = os.getenv('BASE_PATH', '/api/v1/ingest')

    # Check if API-server is alive
    if not IsReachable(backend_host=backend_host, backend_port=backend_port).check():
        print('API-server unreachable: Iprox scraper aborted', flush=True)
        sys.exit(1)

    # Setup UserAuthorization Header
    token = AESCipher(str(uuid4()), os.getenv('AES_SECRET')).encrypt()
    headers = {'Accept': 'application/json', 'IngestAuthorization': token}

    iprox_ingestion = IproxIngestion(backend_host=backend_host, backend_port=backend_port, base_path=base_path,
                                     headers=headers)
    for project_type in ['projects', 'stadsloket']:
        iprox_ingestion.start(project_type)

        # Call Garbage collector
        if garbage_collect is True:
            url = 'http://{host}:{port}/api/v1/ingest/garbagecollector'.format(host=backend_host, port=backend_port)
            result = requests.get(url, headers=headers, params={'project_type': project_type}, timeout=10)
            if result.status_code != 200:
                logger.error(result.text)


if __name__ == '__main__':
    # Call the main entry point for the Iprox scraper
    main()
