# app.py
from flask import Flask, render_template, request, redirect, url_for
from data_base import connect_db

app = Flask(__name__)

# CRUD para Músicas
@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM musica")
    musicas = cursor.fetchall()
    conn.close()
    return render_template('index.html', musicas=musicas)

@app.route('/musica/adicionar', methods=['GET', 'POST'])
def adicionar_musica():
    if request.method == 'POST':
        titulo = request.form['titulo']
        artista = request.form['artista']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO musica (titulo, artista) VALUES (?, ?)", (titulo, artista))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('musica.html')

@app.route('/musica/editar/<int:id>', methods=['GET', 'POST'])
def editar_musica(id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        titulo = request.form['titulo']
        artista = request.form['artista']

        cursor.execute("UPDATE musica SET titulo = ?, artista = ? WHERE id = ?", (titulo, artista, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM musica WHERE id = ?", (id,))
    musica = cursor.fetchone()
    conn.close()
    return render_template('musica.html', musica=musica)

@app.route('/musica/deletar/<int:id>', methods=['POST'])
def deletar_musica(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM musica WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# CRUD para Playlists
@app.route('/playlists')
def listar_playlists():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlist")
    playlists = cursor.fetchall()
    conn.close()
    return render_template('playlist.html', playlists=playlists)

@app.route('/playlist/adicionar', methods=['GET', 'POST'])
def adicionar_playlist():
    if request.method == 'POST':
        nome = request.form['nome']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO playlist (nome) VALUES (?)", (nome,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_playlists'))

    return render_template('adicionar_playlist.html')

@app.route('/playlist/editar/<int:id>', methods=['GET', 'POST'])
def editar_playlist(id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']

        cursor.execute("UPDATE playlist SET nome = ? WHERE id = ?", (nome, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_playlists'))

    cursor.execute("SELECT * FROM playlist WHERE id = ?", (id,))
    playlist = cursor.fetchone()
    conn.close()
    return render_template('adicionar_playlist.html', playlist=playlist)

@app.route('/playlist/deletar/<int:id>', methods=['POST'])
def deletar_playlist(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM playlist WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_playlists'))

# Relacionamento entre Playlists e Músicas
@app.route('/playlist/<int:playlist_id>/musicas')
def listar_musicas_playlist(playlist_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Obter informações da playlist
    cursor.execute("SELECT nome FROM playlist WHERE id = ?", (playlist_id,))
    playlist = cursor.fetchone()

    # Obter músicas associadas à playlist
    cursor.execute('''
    SELECT m.id, m.titulo, m.artista FROM musica m
    JOIN playlist_musica pm ON m.id = pm.musica_id
    WHERE pm.playlist_id = ?
    ''', (playlist_id,))
    musicas = cursor.fetchall()
    
    conn.close()
    return render_template('musicas_playlist.html', playlist=playlist, musicas=musicas, playlist_id=playlist_id)

@app.route('/playlist/<int:playlist_id>/adicionar_musica', methods=['GET', 'POST'])
def adicionar_musica_playlist(playlist_id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        musica_id = request.form['musica_id']
        cursor.execute("INSERT INTO playlist_musica (playlist_id, musica_id) VALUES (?, ?)", (playlist_id, musica_id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_musicas_playlist', playlist_id=playlist_id))

    # Obter lista de músicas para selecionar
    cursor.execute("SELECT * FROM musica")
    musicas = cursor.fetchall()
    conn.close()
    return render_template('adicionar_musica_playlist.html', musicas=musicas, playlist_id=playlist_id)

if __name__ == '__main__':
    app.run(debug=True)
