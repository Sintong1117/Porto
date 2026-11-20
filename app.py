import os
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Kredensial DB diambil dari Environment Variable Kubernetes
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'app')
DB_USER = os.environ.get('DB_USER', 'app')
DB_PASS = os.environ.get('DB_PASS', 'password')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )

@app.route('/')
def index():
    # Buat tabel jika belum ada
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS buku_tamu (id SERIAL PRIMARY KEY, nama VARCHAR(100), pesan TEXT);')
    conn.commit()
    
    # Ambil data dari database
    cur.execute('SELECT nama, pesan FROM buku_tamu ORDER BY id DESC;')
    pesan_masuk = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('index.html', pesan_masuk=pesan_masuk)

@app.route('/kirim_pesan', methods=['POST'])
def kirim_pesan():
    nama = request.form['nama']
    pesan = request.form['pesan']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO buku_tamu (nama, pesan) VALUES (%s, %s)', (nama, pesan))
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect('/#contact') # Kembali ke bagian kontak

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)