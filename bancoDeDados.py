import sqlite3

conn = sqlite3.connect("focusbanco.db")
cursor = conn.cursor()

cursor.execute ('''
    CREATE TABLE IF NOT EXISTS Usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )

''')

conn.commit()

cursor.execute ('''
    CREATE TABLE IF NOT EXISTS Objetivo (
        id INTERGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        titulo TEXT NOT NULL,
        descricao TEXT,
        status TEXT DEFAULT 'pendente',
        prazo DATE,
        FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
    ) 

''')
conn.commit()


cursor.execute ('''
    CREATE TABLE IF NOT EXISTS progresso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        objetivo_id INTEGER NOT NULL,
        porcentagem INTEGER DEFAULT 0,
        tempo_total INTEGER DEFAULT 0,
        FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
        FOREIGN KEY (objetivo_id) REFERENCES Objetivo(id)
    )
''')
conn.commit()
