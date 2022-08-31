.PHONY: build style

build:
	docker build -t funny-tweets-re:one-off --target ONE_OFF . &&\
		docker build -t funny-tweets-re:scheduled --target SCHEDULED .

format:
	@black .

lint: 
	@flake8 .

style: format lint

.PHONY: start generate_token get_twitter_user_id test_one_off test_scheduled

generate_token:
	poetry run python scripts/generate_token.py

get_twitter_user_id:
	poetry run python scripts/get_twitter_user_id.py

start:
	poetry run python src/main.py

test_one_off:
	docker run --env-file .env funny-tweets-re:one-off

test_scheduled:
	docker run --env-file .env funny-tweets-re:scheduled

test:
	poetry run pytest