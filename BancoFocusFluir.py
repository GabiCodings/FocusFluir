import sqlite3


conn = sqlite3.connect("focusfluir.db")
cursor = conn.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS sessoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    duracao_estudo INTEGER NOT NULL,
    duracao_pausa INTEGER NOT NULL,
    playlist_id INTEGER,
    meditacao BOOLEAN DEFAULT 0,
    FOREIGN KEY (playlist_id) REFERENCES playlists(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS objetivos_sessao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sessao_id INTEGER,
    descricao TEXT NOT NULL,
    concluido BOOLEAN DEFAULT 0,
    FOREIGN KEY (sessao_id) REFERENCES sessoes(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS progresso_sessoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sessao_id INTEGER NOT NULL,
    total_objetivos INTEGER DEFAULT 0,
    concluidos INTEGER DEFAULT 0,
    porcentagem INTEGER DEFAULT 0,
    FOREIGN KEY (sessao_id) REFERENCES sessoes(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS playlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    imagem TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS musicas_playlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playlist_id INTEGER NOT NULL,
    titulo TEXT,
    url TEXT NOT NULL,
    FOREIGN KEY (playlist_id) REFERENCES playlists(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS configuracoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duracao_padrao_estudo INTEGER DEFAULT 25,
    duracao_padrao_pausa INTEGER DEFAULT 5,
    playlist_padrao_id INTEGER,
    usar_meditacao BOOLEAN DEFAULT 0,
    FOREIGN KEY (playlist_padrao_id) REFERENCES playlists(id)
);
""")

conn.commit()


# models


def criar_sessao(duracao_estudo, duracao_pausa, playlist_id=None, meditacao=False):
    cursor.execute("""
        INSERT INTO sessoes (duracao_estudo, duracao_pausa, playlist_id, meditacao)
        VALUES (?, ?, ?, ?)
    """, (duracao_estudo, duracao_pausa, playlist_id, meditacao))
    conn.commit()
    return cursor.lastrowid

def adicionar_objetivo(sessao_id, descricao):
    cursor.execute("""
        INSERT INTO objetivos_sessao (sessao_id, descricao)
        VALUES (?, ?)
    """, (sessao_id, descricao))
    conn.commit()

def marcar_objetivo_concluido(objetivo_id):
    cursor.execute("UPDATE objetivos_sessao SET concluido = 1 WHERE id = ?", (objetivo_id,))
    conn.commit()

def salvar_progresso(sessao_id):
    cursor.execute("SELECT COUNT(*), SUM(concluido) FROM objetivos_sessao WHERE sessao_id = ?", (sessao_id,))
    total, concluidos = cursor.fetchone()
    concluidos = concluidos or 0
    porcentagem = int((concluidos / total) * 100) if total > 0 else 0
    cursor.execute("""
        INSERT INTO progresso_sessoes (sessao_id, total_objetivos, concluidos, porcentagem)
        VALUES (?, ?, ?, ?)
    """, (sessao_id, total, concluidos, porcentagem))
    conn.commit()

def criar_playlist(nome, imagem=None):
    cursor.execute("INSERT INTO playlists (nome, imagem) VALUES (?, ?)", (nome, imagem))
    conn.commit()
    return cursor.lastrowid

def adicionar_musica(playlist_id, titulo, url):
    cursor.execute("""
        INSERT INTO musicas_playlist (playlist_id, titulo, url)
        VALUES (?, ?, ?)
    """, (playlist_id, titulo, url))
    conn.commit()

def atualizar_configuracoes(estudo, pausa, playlist_id=None, meditacao=False):
    cursor.execute("DELETE FROM configuracoes")  # Sempre mantém uma só
    cursor.execute("""
        INSERT INTO configuracoes (duracao_padrao_estudo, duracao_padrao_pausa, playlist_padrao_id, usar_meditacao)
        VALUES (?, ?, ?, ?)
    """, (estudo, pausa, playlist_id, meditacao))
    conn.commit()


