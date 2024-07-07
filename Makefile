install:
	@asdf install
	@poetry install
	@poetry run pre-commit install

format-lint:
	@poetry run ruff format
	@poetry ruff check --fix

run:
	@poetry run uvicorn store_api.main:app --reload

test:
	@poetry run pytest