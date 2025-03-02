from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Veritabanına bağlanma fonksiyonu
def get_db_connection():
    conn = sqlite3.connect('scout_app.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ana Sayfa (Sıralama Sayfası)
@app.route('/')
def index():
    return redirect(url_for('siralama'))  # Ana sayfa sıralama sayfasına yönlendirecek

# Sıralama Sayfası (Toplam Puanları Gösterme)
@app.route('/siralama')
def siralama():
    conn = get_db_connection()
    takimlar = conn.execute('SELECT takim_no, toplam_puan FROM takim_puanlar ORDER BY toplam_puan DESC').fetchall()
    conn.close()
    return render_template('siralama.html', takimlar=takimlar)

# İstatistik Sayfası (Yeni Maç Ekleme ve Puan Hesaplama)
@app.route('/istatistik', methods=['GET', 'POST'])
def istatistik():
    if request.method == 'POST':
        takim_no = request.form['takim_no']
        hareket = 3 if 'hareket' in request.form else 0

        otonomSeviye0 = int(request.form['otonomseviye0'])
        otonomSeviye1 = int(request.form['otonomseviye1'])
        otonomSeviye2 = int(request.form['otonomseviye2'])
        otonomSeviye3 = int(request.form['otonomseviye3'])

        seviye0 = int(request.form['seviye0'])
        seviye1 = int(request.form['seviye1'])
        seviye2 = int(request.form['seviye2'])
        seviye3 = int(request.form['seviye3'])

        toplam_puan = hareket + otonomSeviye0 + otonomSeviye1 + otonomSeviye2 + otonomSeviye3 + seviye0 + seviye1 + seviye2 + seviye3

        conn = get_db_connection()
        
        # Aynı takım numarasına sahip bir kayıt varsa, puanları güncelle
        conn.execute('''
            INSERT INTO takim_puanlar (takim_no, toplam_puan)
            VALUES (?, ?)
            ON CONFLICT(takim_no)
            DO UPDATE SET toplam_puan = toplam_puan + ?
        ''', (takim_no, toplam_puan, toplam_puan))
        
        conn.commit()
        conn.close()
        return redirect(url_for('siralama'))  # Yeni maç eklendikten sonra sıralama sayfasına yönlendir
    
    return render_template('istatistik.html')

# Veritabanını oluşturma
def create_db():
    conn = sqlite3.connect('scout_app.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS takim_puanlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            takim_no INTEGER UNIQUE,
            toplam_puan INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Uygulamayı başlat
if __name__ == '__main__':
    create_db()
    app.run(debug=False,host='0.0.0.0')
