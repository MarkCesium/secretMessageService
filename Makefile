.PHONY: dev prod down logs format check

dev:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build

prod:
	docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d --build

down:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml -f docker-compose.prod.yaml down

logs:
	docker compose logs -f

format:
	cd backend && uv run ruff check --fix .
	cd backend && uv run ruff format .

check:
	cd backend && uv run ruff check src
	cd backend && uv run mypy src
