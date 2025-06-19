.PHONY: all simulator edge broker api airflow frontend up

all: simulator edge broker api airflow frontend up

simulator:
 cd simulator && docker build -t simulator .

edge:
 cd edge/edge-ingest && docker build -t edge-ingest .

broker:
 docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto:2

api:
 cd api && docker build -t energia-api .

airflow:
 cd airflow && docker build -t energia-airflow .

frontend:
 cd frontend && docker build -t energia-frontend .

up:
 docker-compose -f deploy/docker-compose.local.yml up -d
