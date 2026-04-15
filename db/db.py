import sqlite3

DATABASE = "focusfluir.db"

def conexao():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def buscar_musicas_da_playlist(playlist_id: int):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT titulo, url 
        FROM musicas_playlist 
        WHERE playlist_id = ?
    """, (playlist_id,))
    
    rows = cursor.fetchall()

    musicas = [
        {"titulo": row["titulo"], "url": row["url"]}
        for row in rows
    ]

    conn.close()
    return musicas


def deletar_playlist(playlist_id: int, id:int):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM musicas_playlist WHERE playlist_id = ?", (playlist_id,))
    cursor.execute("DELETE FROM playlists WHERE id = ?", (playlist_id,))
    conn.commit()
    conn.close()

def listar_playlists():
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM playlists")
    playlist = cursor.fetchall()
    conn.close()
    return playlist