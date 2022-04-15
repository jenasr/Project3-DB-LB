#! /usr/bin/env python3

"""Microservice 3: Tracking users' wins and losses"""

import contextlib
import sqlite3
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field


class Guesses(BaseModel):
        guess1: int = Field(alias='1')
        guess2: int = Field(alias='2')
        guess3: int = Field(alias='3')
        guess4: int = Field(alias='4')
        guess5: int = Field(alias='5')
        guess6: int = Field(alias='6')
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
    with contextlib.closing(sqlite3.connect("DB/stats.db", check_same_thread=False)) as db:
        db.row_factory = sqlite3.Row
        yield db


app = FastAPI()


@app.post("/stats/games/{game_id}")
async def add_game_played(game_id: int, user_id: int, result: Result, db: sqlite3.Connection = Depends(get_db)):
    """Posting a win or loss"""
    # post into games
    cur = db.execute("SELECT user_id FROM users WHERE user_id = ?", [user_id])
    looking_for = cur.fetchall()
    if not looking_for:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    cur = db.execute("SELECT game_id, user_id FROM games WHERE game_id = ? AND user_id = ?", [game_id, user_id])
    looking_for = cur.fetchall()
    if looking_for:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Game for player laready exists"
        )
    cur = db.execute("INSERT INTO games VALUES(?,?,?,?,?)", [user_id, game_id, result.timestamp, result.number_of_guesses, result.status])
    db.commit()
    return result

@app.get("/stats/games/{user_id}/")
async def retrieve_player_stats(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Getting stats of a user"""
    # use table: games
    cur = db.execute("SELECT user_id FROM users WHERE user_id = ?", [user_id])
    looking_for = cur.fetchall()
    if not looking_for:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    # ??????
    # currentStreak = streak at MAX(Date) if the DATE is the same day otherwise 0
    #???????
    cur = db.execute("SELECT streak, MAX(finished) FROM streaks WHERE user_id = ?", [user_id])
    currentStreak = cur.fetchall()[0][0]

    # maxStreak = MAX(streak)
    cur = db.execute("SELECT ending FROM streaks WHERE user_id = ?", [user_id])
    maxStreak = cur.fetchall()[0][0]
    # guesses: for each get the COUNT(each game they had n number of guesses)
    guess_list = []
    int i = 1
    while len(guess_list) < 6:
        cur = db.execute("SELECT COUNT(game_id) FROM games WHERE user_id = ? AND guesses = ?", [user_id, i])
        guess = cur.fetchall()[0][0]
        guess_list.append(guess)
        i += 1
    # need to get failed: COUNT(games lost)
    cur = db.execute("SELECT COUNT(game_id) FROM games WHERE user_id = ? AND won = ?", [user_id, False])
    gamesWon = cur.fetchall()[0][0]    
    # winPercentage: COUNT(wins) / COUNT(games player by user)
    # gamesPlayed:  COUNT(games player by user)
    # gamesWon: COUNT(wins)
    cur = db.execute("SELECT COUNT(game_id) FROM games WHERE user_id = ?", [user_id])
    gamesPlayed = cur.fetchall()[0][0]
    cur = db.execute("SELECT COUNT(game_id) FROM games WHERE user_id = ? AND won = ?", [user_id, True])
    gamesWon = cur.fetchall()[0][0]
    winPercentage = (gamesWon / gamesPlayed) * 100

    # averageGuesses: guesses.items / 6
    averageGuesses = sum(guess_list) / 6
    pass


@app.get("/stats/wins/")
async def retrieve_top_wins(db: sqlite3.Connection = Depends(get_db)):
    """Getting the top 10 users by number of wins"""
    # use view: wins
    # How coudl I also get their number of wins??????????
    cur = db.execute("SELECT username FROM users NATURAL JOIN wins LIMIT 10")
    looking_for = cur.fetchall()
    return {"TopWinners": looking_for}

@app.get("/stats/streaks/")
async def retrieve_top_streaks(db: sqlite3.Connection = Depends(get_db)):
    """Getting the top 10 users by streak"""
    # use view: streaks
    cur = db.execute("SELECT username, streak FROM users NATURAL JOIN streaks ORDER BY streak DESC LIMIT 10")
    looking_for = cur.fetchall()
    return {"TopStreaks": looking_for}
