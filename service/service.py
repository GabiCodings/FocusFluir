import db.db as db

musicas = []
def buscar_musicas_playlist (playlist_id):
    musicas = db.buscar_musicas_da_playlist(playlist_id)
    
    return {
        "musicas": musicas,
        "status": bool(musicas)
    }

def deletar_playlist_service(playlist_id):
    if (playlist_id):
        return db.deletar_playlist
    else:
        return ValueError

