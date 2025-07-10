import pytest
import sqlite3


from BancoFocusFluir import (
    adicionar_musica,
    criar_playlist
    
)

def test_adicionar_musica():
    id_playlist = criar_playlist("Playlist Música Teste", None)
    adicionar_musica("Música", "youtube.com")


