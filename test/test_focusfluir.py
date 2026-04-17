import pytest
from unittest.mock import patch
from app import app
from service import service

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestService:
    @patch('app.service.deletar_playlist_service')
    def test_deletar_playlist_route_sucesso(self, mock_service, client):
        response = client.get('/deletar_playlist/1')

        mock_service.assert_called_once_with(1)
        assert response.status_code == 302
        assert '/playlists' in response.location

    
    def test_deletar_playlist_id_invalido(self):
        with pytest.raises(ValueError) as exc:
            service.deletar_playlist_service(-1)

            assert str(exc.value) == "ID Inválido"



    @patch('service.service.db.buscar_musicas_da_playlist')
    def test_buscar_musicas_playlist_sem_resultado(self, mock_db):
        mock_db.return_value = []

        resultado = service.buscar_musicas_playlist(1)

        mock_db.assert_called_once_with(1)
        assert resultado["status"] == False
        assert resultado["musicas"] == []

    @patch('service.service.db.buscar_musicas_da_playlist')
    def test_buscar_musicas_playlist_resultado(self, mock_svc):
            mock_svc.return_value = [
            {"titulo": "Musica 1", "url": "url1"},
            {"titulo": "Musica 2", "url": "url2"}
        ]

            resultado = service.buscar_musicas_playlist(1)

            mock_svc.assert_called_once_with(1)
            assert resultado["status"] == True
            assert resultado["musicas"] == [
            {"titulo": "Musica 1", "url": "url1"},
            {"titulo": "Musica 2", "url": "url2"}
        ]
