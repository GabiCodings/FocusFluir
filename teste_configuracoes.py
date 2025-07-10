import pytest
import sqlite3

from BancoFocusFluir import set_configuracoes, get_configuracoes

def teste_configuracoes():
    estudo = 1200
    pausa = 300 
    playlist_id = None
    meditacao = True

    set_configuracoes(estudo,pausa,playlist_id, meditacao)

    config = get_configuracoes()

    assert config is not None
    assert config[0] == estudo
    assert config[1] == pausa
    assert config[2] == playlist_id
    assert config[3] == int(meditacao)