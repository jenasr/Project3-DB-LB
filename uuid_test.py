#! /usr/bin/env python3
# sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
    # convert byte string to python type
    # Do we replace GUID with INT ?????????
    # Do we need to change GUID ?????????????????????
# sqlite3.register_adapter(uuid.UUID, lambda u: buffer(u.bytes_le))
    # Convert python type to sqlite supported type

# conn = sqlite3.connect('test.db', detect_types=sqlite3.PARSE_DECLTYPES)
    # In order to use these types we must use the detect types argument

import sqlite3
import uuid

sqlite3.register_converter('INT', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)

conn = sqlite3.connect('test.db', detect_types=sqlite3.PARSE_DECLTYPES)

c = conn.cursor()
c.execute('CREATE TABLE test (guid INT PRIMARY KEY, name TEXT)')

data = (uuid.uuid4(), 'foo')
print('Input Data:', data)
c.execute('INSERT INTO test VALUES (?,?)', data)

c.execute('SELECT * FROM test')
print(f'Result Data: {c.fetchone()}')
