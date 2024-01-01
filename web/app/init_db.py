import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, image_path TEXT)''')
    # Insert admin user
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', '/path/to/image')")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
