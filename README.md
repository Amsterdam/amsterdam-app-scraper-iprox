# Iprox Scraper
The Iprox system feeds content to the https://amsterdam.nl site. This content can also be retrieved in an obscure 
recursive json format. The Iprox scraper reads this json and transforms it into a predictable and reliable data format.
The transformed data can be ingested in a backend of your choosing. See API ingest routes below.

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
    
### Create container on m1 arch for amd64

    docker buildx build --platform=linux/amd64 -f build-docker-image/Dockerfile . -t registry-ams.app-amsterdam.nl/backend-iprox:tst-latest
    docker buildx build --platform=linux/amd64 -f build-docker-image/Dockerfile . -t registry-ams.app-amsterdam.nl/backend-iprox:prd-latest

### Run pylinter

    pylint $(find . -name '*.py' | grep -v -e venv -e migrations -e kladblok)

# Execute
You can start the Iprox scraper with the command below. If the scraper cannot find the TARGET server within 60 seconds 
the container stops. Once the whole scraper process is done, this container will stop too. Hence, the docker image is 
meant to run as a scheduled job, for example using a kubernetes CronJob resource 
(https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/ ) 

You can point to an TARGET server of your choosing by passing the environment parameter
TARGET with the docker run command. This can either be a fully qualified domain name or ip-address. You can also pass
a TARGET-PORT parameter. The ingestion routes on the API-server are protected via a http header token. A secret for 
creating this header (and accepting it on the TARGET) must be given in the docker environment parameter AES_SECRET

    AES_SECRET: A shared secret (required)
    TARGET: FQDN or ip address of the recieving end (default: api-server)
    TARGET_PORT: The tcp port on the recieving end (default: 8000)
    GARBAGE_COLLECT: boolean, enable garbage collecting on recieving end (default: True)
    BASE_PATH: The prepended path for each API on the recieving end (default: /api/v1/ingest) 

    docker run -e TARGET=<FQDN or ip-address> TARGET_PORT=<int> -e AES_SECRET='<API-server secret>' iprox-scraper 

# API ingest routes
The Iprox scraper make use of the following ingestion routes on the TARGET server. All data is JSON formatted and image
data is base64 encoded. BASE_PATH is set via the environment parameter passed to the Docker container and defaults to
'/api/v1/ingest'

    <BASE_PATH>/image            
    <BASE_PATH>/citycontact
    <BASE_PATH>/cityoffice
    <BASE_PATH>/cityoffices

    <BASE_PATH>/project
    <BASE_PATH>/projects
    <BASE_PATH>/news

    <BASE_PATH>/garbagecollector

# Dependencies
This software works in conjunction with https://github.com/Amsterdam/amsterdam-app-backend as a TARGET, but this can
be any TARGET of your choosing.
