from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from datetime import datetime, timezone
from config import MONGO_URL, DB_NAME

# Create connection once at module level
try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # Verify connection on startup
    db = client[DB_NAME]
    scans_collection = db["scans"]
    print(f"[DB] Connected to MongoDB: {DB_NAME}")
except ConnectionFailure as e:
    print(f"[DB] Could not connect to MongoDB: {e}")
    raise


def save_scan(data: dict) -> str:
    """
    Saves a fridge scan result to the 'scans' collection.

    Args:
        data: Dict containing items, expiry, and recipes.

    Returns:
        Inserted document ID as a string, or None on failure.

    Raises:
        PyMongoError: If the insert operation fails.
    """

    try:
        document = {
            "items":     data.get("items", []),
            "expiry":    data.get("expiry", {}),
            "recipes":   data.get("recipes", []),
            "timestamp": datetime.now(timezone.utc),
        }

        result = scans_collection.insert_one(document)
        print(f"[DB] Scan saved with ID: {result.inserted_id}")
        return str(result.inserted_id)

    except PyMongoError as e:
        print(f"[DB] Failed to save scan: {e}")
        raise