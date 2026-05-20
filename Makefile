.PHONY: test lint type cov complexity all

test:
	pytest -v

cov:
	pytest --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=85

lint:
	ruff check src/

type:
	mypy --strict src/

complexity:
	radon cc src/ -s -a -nb

all: lint type test cov complexity
