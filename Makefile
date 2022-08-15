.PHONY: start generate_token get_twitter_user_id

generate_token:
	poetry run python scripts/generate_token.py

get_twitter_user_id:
	poetry run python scripts/get_twitter_user_id.py

start:
	poetry run python src/main.py