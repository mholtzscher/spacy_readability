setup:
	poetry install
	poetry run pre-commit install

test:
	poetry run pytest --cov=spacy_readability -q tests/

ci-test:
	poetry run pytest tests/ --cov=spacy_readability --junitxml=junit/test-results.xml
	poetry run codecov

lint:
	poetry run pylint spacy_readability

mypy:
	poetry run mypy spacy_readability

format:
	poetry run black spacy_readability tests