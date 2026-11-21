### 10.1 DbReader (imperative input binding)

```python
from azure_functions_db import DbReader

reader = DbReader(url="%DB_URL%", table="users")
user = reader.get(pk={"id": user_id})  # single row or None
users = reader.query("SELECT * FROM users WHERE active = :active", params={"active": True})  # list of rows or empty list
```

`get()` returns `None` and `query()` returns an empty list when no rows match. The library does not raise for missing data. Applications that require exactly one row should check the result and raise their own not-found response or error. See [`examples/reader_empty_vs_missing.py`](../examples/reader_empty_vs_missing.py) for a minimal SQLite demonstration with local assertions.

### 10.2 DbWriter (imperative output binding)