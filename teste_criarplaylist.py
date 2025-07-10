import pytest
import sqlite3
from BancoFocusFluir import (
    criar_playlist,
    
)

def test_criar_playlist():
    id_playlist = criar_playlist("Minha Playlist de Teste", "imagem.png")
    assert isinstance(id_playlist, int) and id_playlist > 0

