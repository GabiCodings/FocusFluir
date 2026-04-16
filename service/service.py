import db.db as db

musicas = []
def buscar_musicas_playlist (playlist_id):
    musicas = db.buscar_musicas_da_playlist(playlist_id)
    
    return {
        "musicas": musicas,
        "status": bool(musicas)
    }

def deletar_playlist_service(playlist_id):
    if not isinstance(playlist_id, int) or playlist_id <= 0:
        raise ValueError("ID Inválido")
    db.deletar_playlist(playlist_id, playlist_id)

