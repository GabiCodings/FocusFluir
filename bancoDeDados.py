import sqlite3

conn = sqlite3.connect("focusbanco.db")
cursor = conn.cursor()

cursor.execute ('''
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )

''')

conn.commit()

cursor.execute ('''
    CREATE TABLE IF NOT EXISTS objetivo (
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

cursor.execute ('''
    CREATE TABLE IF NOT EXISTS musicas_favoritas
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    url TEXT NOT NULL,
    tipo TEXT DEFAULT 'youtube',
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)

''')
conn.commit()

cursor.execute ('''
    CREATE TABLE IF NOT EXISTS sessoes
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    data_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    duracao_estudo INTEGER NOT NULL,
    duracao_pausa INTEGER NOT NULL,
    ciclos_completos INTEGER DEFAULT 1,
    anotacoes TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
''')
conn.commit()