#! usr/bin/env python3

"""Microservice 3: Tracking users' wins and losses"""

import contextlib
import sqlite3
from fastapi import FastAPI, Depends, HTTPException, status

def get_db():
    """Connect words.db"""
    with contextlib.closing(sqlite3.connect("words.db", check_same_thread=False)) as db:
        db.row_factory = sqlite3.Row
        yield db


app = FastAPI()



# Posting win or loss: json: {status, timestamp, # of guesses}
# Getting stats of user:
    # json{currentStreak, maxSreak, guesses, 1-6, fail, etc.}
# Getting the top 10 user by number of wins
# Getting the top 10 users by streak
# Seems like we only need a post and 3 gets for this MC.
