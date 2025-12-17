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

    CREATE TABLE IF NOT EXISTS configuracoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        duracao_padrao_estudo INTEGER DEFAULT 1500,  -- 25 min
        duracao_padrao_pausa  INTEGER DEFAULT 300,   -- 5 min
        playlist_padrao_id INTEGER,
        usar_meditacao BOOLEAN DEFAULT 0,
        FOREIGN KEY (playlist_padrao_id) REFERENCES playlists(id)
    )
    """)
    conn.commit()
    conn.close()


# MODELS


# Playlists 
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

@app.route('/sessao')
def sessao():
    return render_template('sessao.html')

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)










