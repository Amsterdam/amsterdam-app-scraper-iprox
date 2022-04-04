#!/bin/sh

#
# DOCKER ENTRY SCRIPT FOR STARTING UP THE AMSTERDAM APP Iprox Scraper
#

start_scraper () {
    printf "Starting Iprox Scraper\n\n"
    cd /code && python main.py
}

start_scraper
