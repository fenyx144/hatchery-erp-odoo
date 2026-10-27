.PHONY: up down

up:
	bash scripts/ensure-dev-secrets.sh
	docker compose up -d --build --wait --remove-orphans

down:
	docker compose down
