import sqlite3

def add_quest(title, difficulty):
    xp_dict = {"Easy": 15, "Medium": 30, "Hard": 50}
    xp = xp_dict.get(difficulty, 20)
    
    conn = sqlite3.connect("data/study_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO quests (title, difficulty, xp, completed) VALUES (?, ?, ?, 0)", 
              (title, difficulty, xp))
    conn.commit()
    conn.close()

def get_quests():
    conn = sqlite3.connect("data/study_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM quests")
    quests = c.fetchall()
    conn.close()
    return quests

def complete_quest(quest_id):
    conn = sqlite3.connect("data/study_data.db")
    c = conn.cursor()
    c.execute("SELECT xp FROM quests WHERE id=?", (quest_id,))
    result = c.fetchone()
    if result:
        xp = result[0]
        c.execute("UPDATE quests SET completed=1 WHERE id=?", (quest_id,))
        conn.commit()
        conn.close()
        return xp
    return 0
