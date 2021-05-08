#!/usr/bin/env bash

##########################################################
### Wrapper script to call the vue docker container    ###    
##########################################################

docker-compose run vue "${@}" 
