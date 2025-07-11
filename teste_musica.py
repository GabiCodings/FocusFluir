import pytest
import sqlite3


from BancoFocusFluir import (
    musicas_playlist,
    adicionar_musica
    
)

@pytest.fixture
def conexao():
    conn = sqlite3.connect(':memory:')
    musicas_playlist(conn)
    yield conn
    conn.close()

def test_adicionar_musica(conexao):
    adicionar_musica(conexao,"Música", "youtube.com")





    assert  in id_playlist

