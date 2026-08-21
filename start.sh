#!/bin/bash
#set -e

docker stop raw_db_con
docker rm raw_db_con
docker rmi raw_db_im
docker build -f dockerfile_raw_db -t raw_db_im .
docker create --name raw_db_con -p 5433:5432 raw_db_im
docker start raw_db_con


