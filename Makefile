.PHONY: start generate_token

generate_token:
	poetry run python scripts/generate_token.py

start:
	poetry run python src/main.py