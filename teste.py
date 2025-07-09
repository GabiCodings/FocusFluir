import pytest
import sqlite3
from BancoFocusFluir import criar_playlist, listar_playlists

@pytest.fixture
def db_connection(tmp_path):
    db_path = tmp_path / "test_focusfluir.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS playlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        imagem TEXT
    );
    """)
    conn.commit()

    import BancoFocusFluir

    BancoFocusFluir.conn = conn
    BancoFocusFluir.cursor = cursor

    yield conn
    conn.close()

def test_criar_playlist(db_connection):
    playlist_id = criar_playlist("Concentração", "imagem1.jpg")
    assert isinstance(playlist_id, int)

    playlists = listar_playlists()
    assert len(playlists) == 1
    assert playlists[0][1] == "Concentração"
