# Iprox Scraper
The Iprox system feeds content to the https://amsterdam.nl site. This content can also be retrieved in an obscure 
recursive json format. The Iprox scraper reads this json and transforms it into a suitable format for the Amsterdam-App.
The content is ingested into the Amsterdam-App-Backend (API server) via REST calls

# Docker build
Clone this project and in the root folder of this project run the command below to build the docker image.

    docker build -t iprox-scraper -f build-docker-image/Dockerfile .

# Execute
You can start the Iprox scraper with the command below. If the scraper cannot find the API server within 60 seconds the
container stops. Once the whole scraper process is done, this container will stop too. Hence, the docker image is ment
to run as a cron-job. You can point to an API server of your choosing by passing the environment parameter
BACKEND_HOST with the docker run command. This can either be a fully qualified domain name or ip-address.

    docker run -e BACKEND_HOST=<FQDN or ip-address> iprox-scraper 

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
