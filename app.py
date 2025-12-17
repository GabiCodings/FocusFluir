from flask import Flask, render_template, request, redirect, url_for

import sqlite3
from datetime import datetime


app = Flask(__name__)


DATABASE = "focusfluir.db"

def conexao():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def setup_database():
    conn = conexao()
    cursor = conn.cursor()
    

    cursor.executescript("""

    CREATE TABLE IF NOT EXISTS playlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        imagem TEXT
    )
    """)                    

    cursor.executescript("""

    CREATE TABLE IF NOT EXISTS musicas_playlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        playlist_id INTEGER,
        titulo TEXT,
        url TEXT NOT NULL,
        FOREIGN KEY (playlist_id) REFERENCES playlists(id)
    )
    """)

    cursor.executescript("""
                         
    CREATE TABLE IF NOT EXISTS sessoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        duracao_programada_estudo INTEGER NOT NULL,
        duracao_programada_pausa INTEGER NOT NULL,
        playlist_id INTEGER,
        FOREIGN KEY (playlist_id) REFERENCES playlists(id)
    )
    """)


    conn.commit()
    conn.close()




# MODEL
#PLAYLIST
def criar_playlist(nome:str, imagem:str|None=None)->int:
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO playlists (nome, imagem) VALUES (?,?)", (nome, imagem))
    conn.commit()
    playlist_id = cursor.lastrowid
    conn.close()
    return playlist_id

def listar_playlists():
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM playlists")
    playlist = cursor.fetchall()
    conn.close()
    return playlist

def adicionar_musica(playlist_id:int, titulo:str, url:str):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO musicas_playlist (playlist_id, titulo, url) VALUES (?,?,?)",
                   (playlist_id, titulo, url))
    conn.commit()
    conn.close()



#SESSAO

def iniciar_nova_sessao(tempo_estudo: int, tempo_pausa: int, playlist_id: int | None, objetivo_id: int | None) -> int:
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessoes (duracao_programada_estudo, duracao_programada_pausa, playlist_id, objetivo_id) VALUES (?, ?, ?, ?)",
        (tempo_estudo, tempo_pausa, playlist_id, objetivo_id)
    )
    conn.commit()
    sessao_id = cursor.lastrowid
    conn.close()
    return sessao_id





#FLASK
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/playlists', methods=['GET', 'POST'])
def playlists_page():
    
    if request.method == 'POST':
        nome_playlist = request.form['nome_playlist']
        imagem_url = request.form.get('imagem_url', '')
        links_musica_str = request.form['links_musica']
        
        
        playlist_id = criar_playlist(nome_playlist, imagem_url)
        
        
        links = [link.strip() for link in links_musica_str.split('\n') if link.strip()]
        
        for link in links:
            adicionar_musica(
                playlist_id=playlist_id, 
                titulo=link, 
                url=link
            )
            
        
        return redirect(url_for('playlists_page'))

    
    playlists = listar_playlists()
    return render_template('playlists.html', playlists=playlists)

@app.route('/sessao', methods=['GET'])
def sessao():
    playlists = listar_playlists()
    
    return render_template('sessao.html', 
        duracao_estudo="",
        duracao_pausa="",
        playlists=playlists,
        )


@app.route('/iniciar_foco', methods=['POST'])
def iniciar_foco():
    
    try:
        tempo_estudo_min = int(request.form.get('duracao_estudo', 25))
    except ValueError:
        tempo_estudo_min = 25
        
    try:
        tempo_pausa_min = int(request.form.get('duracao_pausa', 5))
    except ValueError:
        tempo_pausa_min = 5

    
    tempo_estudo_seg = tempo_estudo_min * 60
    tempo_pausa_seg = tempo_pausa_min * 60
    
    
    playlist_selecionada_id = request.form.get('playlist_selecionada')
    
    
    sessao_id = iniciar_nova_sessao(
        tempo_estudo=tempo_estudo_seg,
        tempo_pausa=tempo_pausa_seg,
        playlist_id=playlist_selecionada_id,
    )
    
    
    return redirect(url_for('timer', sessao_id=sessao_id))


if __name__ == '__main__':
    setup_database()
    app.run(debug=True)










