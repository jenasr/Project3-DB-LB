#! usr/bin/env python3

"""Microservice 3: Tracking users' wins and losses"""

import contextlib
import sqlite3
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel


class Guesses(BaseModel):
        guess1: int
        guess2: int
        guess3: int
        guess4: int
        guess5: int
        guess6: int
        fail: int
# Edit guess1 to 1, guess2 to 2, etc.
class Stats(BaseModel):
    """Json format for a player stats"""
    currentStreak: int
    maxStreak: int
    guesses: Guesses
    winPercentage: float
    gamesPlayed: int
    gamesWon: int
    averageGuesses: int


def get_db():
    """Connect words.db"""
    with contextlib.closing(sqlite3.connect("words.db", check_same_thread=False)) as db:
        db.row_factory = sqlite3.Row
        yield db


app = FastAPI()


@app.post("")
async def add_game_played(, db: sqlite3.Connection = Depends(get_db)):
    """Posting a win or loss"""
    pass


# Getting stats of user:
    # json{currentStreak, maxSreak, guesses, 1-6, fail, etc.}
# Getting the top 10 user by number of wins
# Getting the top 10 users by streak
# Seems like we only need a post and 3 gets for this MC.
