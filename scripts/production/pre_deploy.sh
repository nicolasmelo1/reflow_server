#!/bin/sh

cp scripts/production/docker-compose.production.yml docker-compose.yml
git add -A
git commit -m "deploy"
