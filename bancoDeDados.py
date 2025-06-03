import sqlite3

conn = sqlite3.connect("focusbanco.db")
cursor = conn.cursor()


cursor.execute ('''
    CREATE TABLE IF NOT EXISTS objetivo_sessao (
        id INTERGER PRIMARY KEY AUTOINCREMENT,
        sessao_id INTEGER,
        titulo TEXT NOT NULL,
        concluido BOOLEAN DEFAULT 0,
        status TEXT DEFAULT 'pendente',
        FOREIGN KEY (sessao_id) REFERENCES sessao(id)
        
       
    ) 

''')
conn.commit()


cursor.execute ('''
    CREATE TABLE IF NOT EXISTS progresso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        objetivo_id INTEGER NOT NULL,
        porcentagem INTEGER DEFAULT 0,
        FOREIGN KEY (objetivo_id) REFERENCES Objetivo(id)
    )
''')
conn.commit()

cursor.execute ('''
    CREATE TABLE IF NOT EXISTS playlist
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    url TEXT NOT NULL,
    tipo TEXT DEFAULT 'youtube',
    

''')
conn.commit()

cursor.execute ('''
    CREATE TABLE IF NOT EXISTS sessoes
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    objetivo_id INTEGER,
    playlist_id INTEGER,
    duracao_estudo INTEGER NOT NULL,
    duracao_pausa INTEGER NOT NULL,
    ciclos_completos INTEGER DEFAULT 1,
    FOREIGN KEY (objetivo_id) REFERENCES objetivo(id),
    FOREIGN KEY (playlist_id) REFERENCES playlist(id)
    
''')
conn.commit()

#Model


def model_objetivo(titulo, descricao, status, prazo):
    cursor.execute("INSERT INTO objetivo (titulo, descricao, status, prazo) VALUES (?, ?, ?, ?)", (titulo, descricao, status, prazo))
    conn.commit()

def model_musicas(titulo, url):
    cursor.execute("INSERT INTO musicas_favoritas (titulo, url, tipo) VALUES (?, ?)", (titulo, url))
    conn.commit()

def model_sessoes(duracao_estudo, duracao_pausa, anotacoes):
    cursor.execute("INSERT INTO sessoes (duracao_estudo, duracao_pausa, anotacoes) VALUES (?, ?, ?)", (duracao_estudo, duracao_pausa, anotacoes))
    conn.commit()