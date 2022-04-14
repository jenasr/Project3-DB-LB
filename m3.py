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

class TopWinner(BaseModel):
    username: str
    wins: int

def get_db():
    """Connect words.db"""
    with contextlib.closing(sqlite3.connect("DB/stats.db", check_same_thread=False)) as db:
        db.row_factory = sqlite3.Row
        yield db


app = FastAPI()


@app.post("/stats/games/{game_id}")
async def add_game_played(user_id: int, result: Result, db: sqlite3.Connection = Depends(get_db)):
    """Posting a win or loss"""
    # post into games
    cur = db.execute("SELECT user_id FROM users JOIN games USING user_id WHERE user_id = ?", [user_id])
    looking_for = cur.fetchall()
    if not looking_for:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    cur = db.execute("SELECT game_id, user_id FROM games WHERE game_id = ? AND user_id = ?", [game_id, user_id])
    looking_for = cur.fetchall()
    if not looking_for:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game for player not found"
        )
    cur = db.execute("INSERT INTO games VALUES(?,?,?,?)", [user_id, game_id, result.timestamp, result.guesses, result.status])
    db.commit()
    return result

@app.get("/stats/games/{user_id}")
async def retrieve_player_stats(result: Result, db: sqlite3.Connection = Depends(get_db)):
    """Getting stats of a user"""
    # use table: games
    cur = db.execute("SELECT user_id FROM users JOIN games USING user_id WHERE user_id = ?", [user_id])
    looking_for = cur.fetchall()
    if not looking_for:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    pass


@app.get("/stats/wins")
async def retrieve_top_wins(db: sqlite3.Connection = Depends(get_db)):
    """Getting the top 10 users by number of wins"""
    # use view: wins
    cur = db.execute("SELECT username FROM users JOIN wins USING user_id LIMIT 10")
    looking_for = cur.fetchall()
    plr: TopWinner
    plr_list = []
    for i in range(len(looking_for)):
        plr.username = looking_for[i][0]
        plr.wins= looking_for[i][1]
        plr_list.append(plr)
    return {"top_wins": plr_list}

@app.get("/stats/streaks")
async def retrieve_top_streaks(result: Result, db: sqlite3.Connection = Depends(get_db)):
    """Getting the top 10 users by streak"""
    # use view: streaks
    pass
