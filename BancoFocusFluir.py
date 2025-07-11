
import sqlite3
from datetime import datetime


conn = sqlite3.connect("focusfluir.db")
cursor = conn.cursor()


cursor.executescript("""

CREATE TABLE IF NOT EXISTS playlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    imagem TEXT
)
""")                    

cursor.executescript("""

CREATE TABLE IF NOT EXISTS musicas_playlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playlist_id INTEGER,
    titulo TEXT,
    url TEXT NOT NULL,
    FOREIGN KEY (playlist_id) REFERENCES playlists(id)
)
""")

cursor.executescript("""

CREATE TABLE IF NOT EXISTS configuracoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duracao_padrao_estudo INTEGER DEFAULT 1500,  -- 25 min
    duracao_padrao_pausa  INTEGER DEFAULT 300,   -- 5 min
    playlist_padrao_id INTEGER,
    usar_meditacao BOOLEAN DEFAULT 0,
    FOREIGN KEY (playlist_padrao_id) REFERENCES playlists(id)
)
""")
conn.commit()


# MODELS


# Playlists 
def criar_playlist(nome:str, imagem:str|None=None)->int:
    cursor.execute("INSERT INTO playlists (nome, imagem) VALUES (?,?)", (nome, imagem))
    conn.commit()
    return cursor.lastrowid

def listar_playlists():
    cursor.execute("SELECT id, nome FROM playlists")
    return cursor.fetchall()

def adicionar_musica(titulo:str, url:str):
    cursor.execute("INSERT INTO musicas_playlist (titulo, url) VALUES (?,?)",
                   (titulo, url))
    conn.commit()

# Configurações 
def set_configuracoes(estudo:int, pausa:int, playlist_id:int|None=None, meditacao:bool=False):
    cursor.execute("DELETE FROM configuracoes")
    cursor.execute(
        "INSERT INTO configuracoes (duracao_padrao_estudo, duracao_padrao_pausa, playlist_padrao_id, usar_meditacao) VALUES (?,?,?,?)",
        (estudo, pausa, playlist_id, int(meditacao))
    )
    conn.commit()

def get_configuracoes():
    cursor.execute("SELECT duracao_padrao_estudo, duracao_padrao_pausa, playlist_padrao_id, usar_meditacao FROM configuracoes LIMIT 1")
    return cursor.fetchone()


def fechar_conexao():
    conn.close()



