#! /usr/bin/env python3
import sqlite3
import uuid
import os.path

sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: memoryview(u.bytes_le))
con = sqlite3.connect(f"user_profiles.db", detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()
cur.execute("SELECT * from users")
print(cur.fetchall())
