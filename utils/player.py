import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("data/study_data.db")
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS player 
                 (id INTEGER PRIMARY KEY, name TEXT, level INTEGER DEFAULT 1, 
                  xp INTEGER DEFAULT 0, streak INTEGER DEFAULT 0, last_date TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS quests 
                 (id INTEGER PRIMARY KEY, title TEXT, difficulty TEXT, 
                  xp INTEGER, completed INTEGER DEFAULT 0)''')
    
    c.execute("SELECT * FROM player WHERE id=1")
    if not c.fetchone():
        today = datetime.now().strftime("%Y-%m-%d")
        c.execute("""INSERT INTO player (id, name, level, xp, streak, last_date) 
                     VALUES (1, 'Shadow Hunter', 1, 0, 0, ?)""", (today,))
    conn.commit()
    conn.close()

def get_player():
    conn = sqlite3.connect("data/study_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM player WHERE id=1")
    player = c.fetchone()
    conn.close()
    return player

def add_xp(xp_gain):
    conn = sqlite3.connect("data/study_data.db")
    c = conn.cursor()
    c.execute("""
        UPDATE player 
        SET xp = xp + ?,
            level = 1 + ((xp + ?) // 100)
        WHERE id=1
    """, (xp_gain, xp_gain))
    conn.commit()
    conn.close()
