import sqlite3

def initiate_trade(from_user, to_user, card_id, status='pending'):
    conn = sqlite3.connect('mystic_realms.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO trades (from_user, to_user, card_id, status)
              VALUES (?, ?, ?, 'pending')
              ''', (from_user, to_user, card_id))
    conn.commit()
    conn.close()