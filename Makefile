.PHONY: dev prod down logs

dev:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build

prod:
	docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d --build

down:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml -f docker-compose.prod.yaml down

logs:
	docker compose logs -f
