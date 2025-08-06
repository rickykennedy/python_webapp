.PHONY: install run dev test export-req

install:
	poetry install

run:
	poetry run flask run --host=0.0.0.0 --port=5000

dev:
	poetry shell

test:
	poetry run pytest

export-req:
	poetry export --without-hashes -f requirements.txt -o requirements.txt
