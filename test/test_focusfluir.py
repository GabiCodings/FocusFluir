import pytest
from unittest.mock import patch
from app import app

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
        assert '/playlists_page' in response.location