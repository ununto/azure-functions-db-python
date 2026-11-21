"""Distinguish empty query results from a missing required row.

This example uses a temporary SQLite database and the public DbReader API
to show:

1. A query that finds a matching row.
2. A query that returns an empty list (no matching rows).
3. An application-level check that raises when exactly one row is required.

The library returns None from get() or an empty list from query() when no
rows match. It does not raise for missing data; callers decide how to treat
that case (return a not-found response, raise an application error, etc.).

Run with:
    python examples/reader_empty_vs_missing.py
"""

from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path

from azure_functions_db import DbReader


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "example.db"
        url = f"sqlite:///{db_path}"

        # Create a minimal table and insert one row.
        with sqlite3.connect(db_path) as conn:
            conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
            conn.execute("INSERT INTO users (id, name) VALUES (1, 'Alice')")
            conn.commit()

        with DbReader(url=url, table="users") as reader:
            # Found row
            found = reader.get(pk={"id": 1})
            assert found is not None
            assert found["name"] == "Alice"
            print("Found:", found)

            # Empty result (no matching row)
            missing = reader.get(pk={"id": 999})
            assert missing is None
            print("Missing row returns:", missing)

            # Query that returns zero rows
            empty = reader.query(
                "SELECT * FROM users WHERE name = :name",
                params={"name": "Bob"},
            )
            assert empty == []
            print("Empty query result:", empty)

            # Application requires exactly one row
            rows = reader.query("SELECT * FROM users WHERE id = :id", params={"id": 42})
            if not rows:
                # Library does not raise; application decides the response.
                print("Application would raise not-found for id=42")
            else:
                print("Unexpected rows:", rows)


if __name__ == "__main__":
    main()
