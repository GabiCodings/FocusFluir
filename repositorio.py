import sqlite3

DATABASE = "focusfluir.db"

def conexao():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

