.PHONY: start generate_token get_twitter_user_id package

generate_token:
	poetry run python scripts/generate_token.py

get_twitter_user_id:
	poetry run python scripts/get_twitter_user_id.py

start:
	poetry run python src/main.py

package:
	docker build -t funny-tweets-re --target PROD .

test_package:
	docker run --env-file .env funny-tweets-re