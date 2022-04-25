#! /usr/bin/env python3
import sqlite3
import uuid
import os.path

column_added = True
def add_uuids():
    sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
    sqlite3.register_adapter(uuid.UUID, lambda u: memoryview(u.bytes_le))
    con = sqlite3.connect(f"DB/stats.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    if not column_added:
        cur.execute("ALTER TABLE users ADD unique_id GUID")
    the_tuples = cur.execute("SELECT * from users")
    user_id_dict = {}
    g_uuid = uuid.uuid1()
    for t in the_tuples:
        a_uuid = uuid.uuid1()
        cur.execute("UPDATE users SET unique_id = ? WHERE user_id = ?", [a_uuid, t[0]])
        con.commit()
    if not column_added:
        cur.execute("ALTER TABLE games ADD unique_id GUID")
    the_tuples = cur.execute("SELECT * FROM games")
    g_uuid = a_uuid
    for t in the_tuples:
        cur.execute("UPDATE games SET unique_id = ? WHERE user_id = ?", [g_uuid, t[0]])
        con.commit()

def sharding():
    sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
    sqlite3.register_adapter(uuid.UUID, lambda u: memoryview(u.bytes_le))
    con1 = sqlite3.connect(f"DB/stats.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur1 = con1.cursor()
    for i in range(3):
        file_exists = os.path.exists(f"DB/Shards/stats{i+1}.db")
        con2 = sqlite3.connect(f"DB/Shards/stats{i+1}.db", detect_types=sqlite3.PARSE_DECLTYPES)
        cur2 = con2.cursor()
        cur1.execute("SELECT * FROM games WHERE unique_id % 3 = ?", [i])
        list1 = cur1.fetchall()
        if not file_exists:
            cur2.execute("""CREATE TABLE games (user_id INTEGER NOT NULL, game_id INTEGER NOT NULL,
                finished DATE DEFAULT CURRENT_TIMESTAMP, guesses INTEGER, won BOOLEAN, unique_id GUID, PRIMARY KEY(user_id, game_id),
                FOREIGN KEY(user_id) REFERENCES users(user_id))""")
            cur2.executemany("INSERT INTO games VALUES(?, ?, ?, ?, ?, ?)", list1)
            con2.commit()
            cur2.execute("CREATE VIEW wins AS SELECT unique_id, COUNT(won) FROM games WHERE won = TRUE GROUP BY unique_id ORDER BY COUNT(won) DESC")
            con2.commit()
            cur2.execute("""CREATE VIEW streaks AS WITH ranks AS (SELECT DISTINCT unique_id, finished, RANK() OVER(PARTITION BY unique_id ORDER BY finished) AS rank FROM
            games WHERE won = TRUE ORDER BY unique_id, finished), groups AS (SELECT unique_id, finished, rank, DATE(finished, '-' || rank || ' DAYS') AS base_date FROM ranks)
            SELECT unique_id, COUNT(*) AS streak, MIN(finished) AS beginning, MAX(finished) AS ending FROM groups GROUP BY unique_id, base_date HAVING streak > 1 ORDER BY
            unique_id, finished""")
            con2.commit()
            cur2.execute("CREATE INDEX games_won_idx ON games(won)")
            con2.commit()
        else:
            print("DB already made")
        con2.close()

    con3 = sqlite3.connect(f"DB/Shards/user_profiles.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur3 = con3.cursor()
    cur1.execute("SELECT * FROM users")
    list1 = cur1.fetchall()
    cur3.execute("CREATE TABLE users(user_id INTEGER PRIMARY KEY, username VARCHAR UNIQUE, unique_id GUID)")
    con3.commit()
    cur3.executemany("INSERT INTO users VALUES(?, ?, ?)", list1)
    con3.close()
    con1.close()



if __name__ == '__main__':
    add_uuids()
    sharding()
    con = sqlite3.connect(f"DB/Shards/stats1.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("SELECT * FROM games LIMIT 10")
    print(cur.fetchall())
