#!/bin/bash
docker-compose rm -f && \
    docker-compose up --force-recreate
