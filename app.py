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
    cursor.execute(
        "INSERT INTO musicas_playlist (playlist_id, titulo, url) VALUES (?,?,?)",
        (playlist_id, titulo, url)
    )
    conn.commit()
    conn.close()

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



def deletar_playlist(playlist_id: int):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM musicas_playlist WHERE playlist_id = ?", (playlist_id,))
    cursor.execute("DELETE FROM playlists WHERE id = ?", (playlist_id,))
    conn.commit()
    conn.close()

def buscar_playlist_por_id(playlist_id: int):
    conn = conexao()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM playlists WHERE id = ?", (playlist_id,))
    playlist = cursor.fetchone()

    cursor.execute("SELECT url FROM musicas_playlist WHERE playlist_id = ?", (playlist_id,))
    musicas = cursor.fetchall()

    conn.close()

    links = "\n".join([m["url"] for m in musicas])

    return {
        "id": playlist["id"],
        "nome": playlist["nome"],
        "links": links
    }

def atualizar_playlist(playlist_id: int, nome: str, links: list):
    conn = conexao()
    cursor = conn.cursor()

    cursor.execute("UPDATE playlists SET nome = ? WHERE id = ?", (nome, playlist_id))
    cursor.execute("DELETE FROM musicas_playlist WHERE playlist_id = ?", (playlist_id,))

    for link in links:
        cursor.execute(
            "INSERT INTO musicas_playlist (playlist_id, titulo, url) VALUES (?, ?, ?)",
            (playlist_id, link, link)
        )

    conn.commit()
    conn.close()

def iniciar_nova_sessao(tempo_estudo: int, tempo_pausa: int, playlist_id: int) -> int:
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessoes (duracao_programada_estudo, duracao_programada_pausa, playlist_id) VALUES (?, ?, ?)",
        (tempo_estudo, tempo_pausa, playlist_id)
    )
    conn.commit()
    sessao_id = cursor.lastrowid
    conn.close()
    return sessao_id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estudo')
def estudo():
    min_foco = request.args.get('min_foco', 25)
    min_pausa = request.args.get('min_pausa', 5)
    playlist_id = request.args.get('playlist_id')
    objetivos = request.args.get('objetivos', '[]')

    musicas = []
    if playlist_id:
        musicas = buscar_musicas_da_playlist(playlist_id)

    return render_template(
        'estudo.html',
        min_foco=min_foco,
        min_pausa=min_pausa,
        musicas=musicas,
        objetivos=objetivos  
    )

@app.route('/playlists', methods=['GET', 'POST'])
def playlists_page():
    edit_playlist = None

    if request.method == 'POST':
        nome_playlist = request.form['nome_playlist']
        links_musica_str = request.form['links_musica']
        edit_id = request.form.get('edit_id')

        links = [link.strip() for link in links_musica_str.split('\n') if link.strip()]

        if edit_id:
            atualizar_playlist(int(edit_id), nome_playlist, links)
        else:
            playlist_id = criar_playlist(nome_playlist)
            for link in links:
                adicionar_musica(playlist_id, link, link)

        return redirect(url_for('playlists_page'))

    edit_id = request.args.get('edit_id')
    if edit_id:
        edit_playlist = buscar_playlist_por_id(int(edit_id))

    playlists = listar_playlists()
    return render_template('playlists.html', playlists=playlists, edit_playlist=edit_playlist)


@app.route('/deletar_playlist/<int:id>')
def deletar_playlist_route(id):
    deletar_playlist(id)
    return redirect(url_for('playlists_page'))

@app.route('/sessao', methods=['GET'])
def sessao():
    playlists = listar_playlists()
    return render_template('sessao.html', playlists=playlists)

@app.route('/iniciar_foco', methods=['POST'])
def iniciar_foco():
    tempo_estudo_min = int(request.form.get('duracao_estudo', 25))
    tempo_pausa_min = int(request.form.get('duracao_pausa', 5))
    playlist_selecionada_id = request.form.get('playlist_id') 
    objetivos = request.form.get('objetivos', '[]')

    iniciar_nova_sessao(
        tempo_estudo=tempo_estudo_min * 60,
        tempo_pausa=tempo_pausa_min * 60,
        playlist_id=playlist_selecionada_id,
    )
    
    return redirect(url_for(
        'estudo',
        min_foco=tempo_estudo_min,
        min_pausa=tempo_pausa_min,
        playlist_id=playlist_selecionada_id,
        objetivos=objetivos 
    ))

@app.route('/relatorio')
def relatorio():
    objetivos = request.args.get('objetivos', '[]')
    concluidos = request.args.get('concluidos', '[]')
    ciclos = request.args.get('ciclos', 0)

    return render_template(
        'relatorio.html',
        objetivos=objetivos,
        concluidos=concluidos,
        ciclos=ciclos
    )

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)