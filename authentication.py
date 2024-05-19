import sqlite3
import hashlib

def register_user(username, password):
    if len(username) < 3 or len(password) < 5:
        return False, "Username must be at least 3 characters and password at least 5 characters."

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        conn = sqlite3.connect('mystic_realms.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password, coins) VALUES (?, ?, ?)', (username, password_hash, 100))
        conn.commit()
        conn.close()
        return True, "User registered successfully."
    except sqlite3.IntegrityError:
        return False, "Username already taken."

def login_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect('mystic_realms.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password_hash))
    user = c.fetchone()
    conn.close()
    
    if user:
        return True, "Login successful."
    else:
        return False, "Invalid username or password."
