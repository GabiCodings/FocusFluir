from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from urllib.request import urlopen
import db.db as db
import service.service as service
import json

app = Flask(__name__)

DATABASE = "focusfluir.db"

def conexao():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def obter_titulo_youtube(url):
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        with urlopen(oembed_url, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data.get("title", url)
    except:
        return url

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


def adicionar_musica(playlist_id:int, titulo:str, url:str):
    conn = conexao()
    cursor = conn.cursor()
    titulo_real = obter_titulo_youtube(url)
    cursor.execute(
        "INSERT INTO musicas_playlist (playlist_id, titulo, url) VALUES (?,?,?)",
        (playlist_id, titulo_real, url)
    )
    conn.commit()
    conn.close()


def buscar_playlist_por_id(playlist_id: int):
    conn = conexao()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM playlists WHERE id = ?", (playlist_id,))
    playlist = cursor.fetchone()

    cursor.execute("SELECT titulo, url FROM musicas_playlist WHERE playlist_id = ?", (playlist_id,))
    musicas = cursor.fetchall()

    links_lista = []
    titulos = []

    for m in musicas:
        url = m["url"]
        titulo = m["titulo"]

        if not titulo or titulo == url:
            titulo = obter_titulo_youtube(url)

            conn2 = conexao()
            c2 = conn2.cursor()
            c2.execute(
                "UPDATE musicas_playlist SET titulo = ? WHERE url = ? AND playlist_id = ?",
                (titulo, url, playlist_id)
            )
            conn2.commit()
            conn2.close()

        links_lista.append(url)
        titulos.append(titulo)

    conn.close()

    links = "\n".join(links_lista)

    return {
        "id": playlist["id"],
        "nome": playlist["nome"],
        "links": links,
        "titulos": titulos
    }

def atualizar_playlist(playlist_id: int, nome: str, links: list, remover_links: list):
    conn = conexao()
    cursor = conn.cursor()

    cursor.execute("UPDATE playlists SET nome = ? WHERE id = ?", (nome, playlist_id))

    cursor.execute("SELECT url FROM musicas_playlist WHERE playlist_id = ?", (playlist_id,))
    musicas_atuais = [row["url"] for row in cursor.fetchall()]

    for link in remover_links:
        cursor.execute(
            "DELETE FROM musicas_playlist WHERE playlist_id = ? AND url = ?",
            (playlist_id, link)
        )

    for link in links:
        if link not in musicas_atuais:
            titulo_real = obter_titulo_youtube(link)
            cursor.execute(
                "INSERT INTO musicas_playlist (playlist_id, titulo, url) VALUES (?, ?, ?)",
                (playlist_id, titulo_real, link)
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

    
    musicas = service.buscar_musicas_playlist(playlist_id)

    return render_template(
        'estudo.html',
        min_foco=min_foco,
        min_pausa=min_pausa,
        musicas=musicas["musicas"],
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
        remover_links = request.form.getlist('remover_musica')

        if edit_id:
            atualizar_playlist(int(edit_id), nome_playlist, links, remover_links)
        else:
            playlist_id = criar_playlist(nome_playlist)
            for link in links:
                adicionar_musica(playlist_id, link, link)

        return redirect(url_for('playlists_page'))

    edit_id = request.args.get('edit_id')
    if edit_id:
        edit_playlist = buscar_playlist_por_id(int(edit_id))

    playlists = db.listar_playlists()
    return render_template('playlists.html', playlists=playlists, edit_playlist=edit_playlist)

@app.route('/deletar_playlist/<int:playlist_id>')
def deletar_playlist_route(playlist_id):
    service.deletar_playlist_service(playlist_id)
    return redirect(url_for('playlists_page'))

@app.route('/sessao')
def sessao():
    playlists = db.listar_playlists()
    return render_template('sessao.html', playlists=playlists)

@app.route('/iniciar_foco', methods=['POST'])
def iniciar_foco():
    tempo_estudo_min = int(request.form.get('duracao_estudo', 0))
    tempo_pausa_min = int(request.form.get('duracao_pausa', 0))
    playlist_selecionada_id = request.form.get('playlist_id') 
    objetivos = request.form.get('objetivos', '[]')

    if tempo_estudo_min <= 0:
        return "Tempo de estudo inválido", 400

    if tempo_pausa_min <= 0:
        return "Tempo de pausa inválido", 400

    try:
        lista_objetivos = json.loads(objetivos)
        if not lista_objetivos:
            return "Adicione pelo menos um objetivo", 400
    except:
        return "Erro nos objetivos", 400

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