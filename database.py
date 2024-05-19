import sqlite3

def init_db():
    conn = sqlite3.connect('mystic_realms.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            coins INTEGER DEFAULT 0
        )
    ''')
    
    # Create cards table
    c.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            rarity TEXT NOT NULL,
            value INTEGER NOT NULL
        )
    ''')

    # Create user_cards table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_cards (
            username TEXT NOT NULL,
            card_id INTEGER NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username),
            FOREIGN KEY (card_id) REFERENCES cards(id)
        )
    ''')
    
    conn.commit()
    conn.close()
