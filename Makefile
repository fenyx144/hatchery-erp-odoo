.PHONY: up down check

up:
	bash scripts/ensure-dev-secrets.sh
	docker compose up -d --build --wait --remove-orphans

check:
	curl -f --cacert secrets/dev-ca.crt https://localhost/api/v1/health

down:
	docker compose down
