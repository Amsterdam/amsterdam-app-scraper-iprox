import os
import requests
from uuid import uuid4
from FetchData.IproxIngestion import IproxIngestion
from GenericFunctions.AESCipher import AESCipher
from GenericFunctions.IsReachable import IsReachable
from GenericFunctions.Logger import Logger


if __name__ == '__main__':
    logger = Logger()
    # Get environment parameters: BACKEND host and port
    backend_host = os.getenv('BACKEND_HOST', 'api-server')
    backend_port = int(os.getenv('BACKEND_PORT', 8000))

    # Check if API-server is alive
    if not IsReachable(backend_host=backend_host, backend_port=backend_port).check():
        print('API-server unreachable: Iprox scraper aborted')
        exit(1)

    # Setup UserAuthorization Header
    token = AESCipher(str(uuid4()), os.getenv('AES_SECRET')).encrypt()
    headers = {'Accept': 'application/json', 'IngestAuthorization': token}

    iprox_ingestion = IproxIngestion(backend_host=backend_host, backend_port=8000, headers=headers)
    for project_type in ['brug', 'kade', 'stadsloket']:
        iprox_ingestion.start(project_type)

        # Call Garbage collector
        url = 'http://{host}:{port}/api/v1/ingest/garbagecollector'.format(host=backend_host, port=backend_port)
        result = requests.get(url, headers=headers, params={'project_type': project_type})
        if result.status_code != 200:
            logger.error(result.text)