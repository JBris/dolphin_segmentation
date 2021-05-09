#!/usr/bin/env bash

##########################################################
### Retrieve the notebook token from Jupyter container ###    
##########################################################

docker-compose logs --tail=50 jupyter | grep token
