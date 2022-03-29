#!/bin/sh

#
# DOCKER ENTRY SCRIPT FOR STARTING UP THE AMSTERDAM APP Iprox Scraper
#

abort () {
  printf '\rAPI-server unreachable: Iprox scraper aborted\n'
  exit 1
}

is_backend_alive () {
  state=0
  count=0
  printf "Checking for API-server"
  while ! nc -q 1 ${BACKEND_HOST} 8000 </dev/null 1> /dev/null 2> /dev/null; do
    case $state in
      0) printf "\Checking for API-server: -";;
      1) printf "\Checking for API-server: \\";;
      2) printf "\Checking for API-server: |";;
      3) printf "\Checking for API-server: /";;
    esac
    [ "${state}" = "3" ] && state=0 || state=$((state+1))
    [ "${count}" = "600" ] && abort || count=$((count+1))
    sleep 0.1
  done
  printf '\rChecking for API-server -> API-server alive\n'
}

set_header () {
    printf "Initializing Amsterdam-App: Iprox scraper\n"
}

start_scraper () {
    printf "Starting Iprox Scraper\n\n"
    cd /code && python main.py
}

set_header
is_backend_alive
start_scraper
