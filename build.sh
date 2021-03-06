#!/usr/bin/env bash

if [ ! -f ".env" ]; then 
    cp .env.example .env 
    echo "If required, please edit .env before continuing. Otherwise, execute build.sh again."
    exit 0
fi

while getopts e opt; do
    case $opt in
        e) 
            cp .env.example .env  
            ;;
        *) 
            exit 1
            ;;
  esac
done

. .env

shift $(($OPTIND - 1))

docker-compose down
docker-compose pull
docker-compose build
docker-compose up -d 

echo
./jupyter_token.sh