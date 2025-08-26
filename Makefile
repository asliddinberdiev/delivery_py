.PHONY: run_dev run_prod pkg_update pkg_install

run_dev:
	uvicorn main:app --reload

run_prod:
	uvicorn main:app --host 0.0.0.0 --port 8000

pkg_update:
	pip freeze > requirements.txt

pkg_install:
	pip install -r requirements.txt

compose-up:
	@docker compose up -d

compose-down:
	@docker compose down