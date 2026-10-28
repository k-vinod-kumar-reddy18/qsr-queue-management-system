.PHONY: up down logs test
up:
	docker compose up --build -d
down:
	docker compose down
logs:
	docker compose logs -f --tail=200
test:
	python -m pytest backend/tests -q
