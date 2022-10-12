#!/bin/sh

#
# DOCKER ENTRY SCRIPT FOR STARTING UP THE AMSTERDAM APP Iprox Scraper
#

start_scraper () {
    if [ -z ${UNITTEST} ]; then
      printf "Starting Iprox Scraper\n\n"
      cd /code && python main.py
    else
      printf "Starting unittests\n\n"
      cd /code && PYTHONPATH=/code pytest --no-header --no-summary -q unittests/
    fi
}

start_scraper
