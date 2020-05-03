from pymongo import MongoClient
from infrastructure.services.services import Services

import settings


def can_connect_mongo() -> bool:
    """Check if mongo is accessible.

    Requires:
        Mongo environment variable are correctly defined.

    Returns:
        True if mongo is accessible, False otherwise.

    """
    try:
        database = "fenrys"
        collection = "event_store"
        collection = MongoClient(
            host=settings.mongo_url(),
            port=27017,
            username=settings.mongo_username(),
            password=settings.mongo_password(),
        )[database][collection]
        collection.find_one()
        return True
    except Exception:
        Services.logger().warning(
            f"Can't connect mongo {settings.mongo_url()} with username {settings.mongo_username()}"
        )
        return False
