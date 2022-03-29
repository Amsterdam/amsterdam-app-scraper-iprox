# Iprox Scraper 
Dit project heeft als doel het scrapen van content uit het Iprox systeem. Iprox voed de webpagina's van 
https://amsterdam.nl. De content uit Iprox word door de scraper door middel van API calls ingested bij de 
Amsterdam-App-Backend. De content wordt op zodanige manier gestructureerd dat het geschikt is voor gebruik in
de Amsterdam-App

# Docker build

    docker build -t iprox-scraper -f build-docker-image/Dockerfile .

# Execute

    docker run -e BACKEND_HOST=<FQDN or ip-address> iprox-scraper 
