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

logs-%:
	docker logs -f $*

frontend-dev:
	cd cloud/frontend && npm install && npm run dev

reset:
	docker-compose down -v --remove-orphans

seed:
	docker exec -it energia-api python seed.py || echo "seed.py no disponible"
	
doctor:
	@echo "🔎 Verificando estructura de servicios..."
	@for dir in simulator edge/edge-ingest api frontend cloud/airflow; do \
		if [ -d "$$dir" ]; then \
		if [ -f "$$dir/Dockerfile" ]; then \
		echo "✅ Dockerfile encontrado en $$dir"; \
		else \
		echo "❌ FALTA Dockerfile en $$dir"; \
            fi; \
        else \
            echo "⚠️  Carpeta $$dir no existe"; \
        fi; \
    done
preview:
	cd frontend && npm install && npm run dev -- --host
