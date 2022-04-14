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
    # Should we add username????????????????
    currentStreak: int
    maxStreak: int
    guesses: Guesses
    winPercentage: float
    gamesPlayed: int
    gamesWon: int
    averageGuesses: int

class Result(BaseModel):
    status: bool
    timestamp: str
    number_of_guesses: int


def get_db():
    """Connect words.db"""
    with contextlib.closing(sqlite3.connect("stats.db", check_same_thread=False)) as db:
        db.row_factory = sqlite3.Row
        yield db


app = FastAPI()


@app.post("")
async def add_game_played(result: Result, db: sqlite3.Connection = Depends(get_db)):
    """Posting a win or loss"""
    # post into games
    pass

@app.get("")
async def retrieve_player_stats(result: Result, db: sqlite3.Connection = Depends(get_db)):
    """Getting stats of a user"""
    # use table: games
    pass

@app.get("")
async def retrieve_top_wins(result: Result, db: sqlite3.Connection = Depends(get_db)):
    """Getting the top 10 users by number of wins"""
    # use view: wins
    pass

@app.get("")
async def retrieve_top_streaks(result: Result, db: sqlite3.Connection = Depends(get_db)):
    """Getting the top 10 users by streak"""
    # use view: streaks
    pass
