import os
import json
import logging

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=os.environ.get("LOGGER_LEVEL", "INFO"),
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)

CONFIG = {
    "adapters": {
        "firebase": {
            "service_account": json.loads(
                os.environ.get("GOOGLE_SERVICE_ACCOUNT"),
                strict=False,
            ),
            "collection_expire_after_days": int(os.environ.get("EXPIRE_AFTER_DAYS", 7)),
        },
        "twitter": {
            "owner_user_id": os.environ.get("OWNER_USER_ID"),
            "consumer_key": os.environ.get("API_KEY"),
            "consumer_secret": os.environ.get("API_SECRET_KEY"),
            "access_token": os.environ.get("ACCESS_TOKEN"),
            "access_token_secret": os.environ.get("ACCESS_TOKEN_SECRET"),
        },
    },
    "schedule_every_hours": int(os.environ.get("SCHEDULE_EVERY_HOURS", 6)),
}
