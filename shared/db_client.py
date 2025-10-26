# shared/db_client.py

import sqlite3

class DatabaseClient:
    """A mock database client for interacting with the SQLite databases."""

    def __init__(self):
        # In a real system, you'd manage connections to multiple DBs
        pass

    def save(self, table_name, data):
        print(f"[DB] Saving to {table_name}: {data}")
        # This would be an INSERT statement
        return "mock_id_123"

    def get(self, table_name, item_id):
        print(f"[DB] Getting {item_id} from {table_name}")
        # This would be a SELECT statement
        return {"id": item_id, "mock_data": "value"}

    def update(self, table_name, item_id, data):
        print(f"[DB] Updating {item_id} in {table_name} with {data}")
        # This would be an UPDATE statement
        return True

# Global DB client instance
db = DatabaseClient()
