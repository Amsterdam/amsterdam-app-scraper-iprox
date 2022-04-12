# Iprox Scraper
The Iprox system feeds content to the https://amsterdam.nl site. This content can also be retrieved in an obscure 
recursive json format. The Iprox scraper reads this json and transforms it into a suitable format for the Amsterdam-App.
The content is ingested into the Amsterdam-App-Backend (API server) via REST calls

# Setup your development environment
Clone this project and in the root folder of this project run the command below to setup your development environment
    
    python3 -m venv venv
    python3 -m pip install -r build-docker-image/requirements.txt

# Unit testing
Make sure you've installed the test-requirements. You can find them in build-docker-image/requirements-unittest.txt

    python3 -m pip install -r build-docker-image/requirements-unittest.txt

Clone this project and in the root folder of this project run the command below to run the unit-tests

    PYTHONPATH=`pwd` pytest --no-header --no-summary -q unittests/

# Docker build
Clone this project and in the root folder of this project run the command below to build the docker image.

    docker build -t iprox-scraper -f build-docker-image/Dockerfile .

# Execute
You can start the Iprox scraper with the command below. If the scraper cannot find the API server within 60 seconds the
container stops. Once the whole scraper process is done, this container will stop too. Hence, the docker image is ment
to run as a cron-job. You can point to an API server of your choosing by passing the environment parameter
BACKEND_HOST with the docker run command. This can either be a fully qualified domain name or ip-address. The ingest
routes on the API-server are protected via a http header token. A secret for creating this header (and accepting it on
the API-server) must be given in the docker environment parameter AES_SECRET

    docker run -e BACKEND_HOST=<FQDN or ip-address> -e AES_SECRET='<API-server secret>' iprox-scraper 

# API ingest routes
The Iprox scraper make use of the following ingestion routes on the API server

    /api/v1/ingest/image
    /api/v1/ingest/citycontact
    /api/v1/ingest/cityoffice
    /api/v1/ingest/cityoffices

    /api/v1/ingest/project
    /api/v1/ingest/projects
    /api/v1/ingest/news

    /api/v1/ingest/garbagecollector

# Dependencies
This software depends on the API-server. You can find the code for this software at 
https://github.com/Amsterdam/amsterdam-app-backend
