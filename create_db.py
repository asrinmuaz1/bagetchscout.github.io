import sqlite3

def create_db():
    conn = sqlite3.connect('istatistik.db')  # Veritabanı dosyasını oluşturun
    c = conn.cursor()

    # Tabloyu oluştur
    c.execute('''
        CREATE TABLE IF NOT EXISTS takim_puanlar (
            takim_no INTEGER PRIMARY KEY,  -- Takım numarası birincil anahtar
            hareket INTEGER DEFAULT 0,  -- Hareket etti mi? Puan
            otonom_seviye0 INTEGER DEFAULT 0,  -- Otonom Seviye 0 Puanı
            otonom_seviye1 INTEGER DEFAULT 0,  -- Otonom Seviye 1 Puanı
            otonom_seviye2 INTEGER DEFAULT 0,  -- Otonom Seviye 2 Puanı
            otonom_seviye3 INTEGER DEFAULT 0,  -- Otonom Seviye 3 Puanı
            seviye0 INTEGER DEFAULT 0,  -- Seviye 0 Puanı
            seviye1 INTEGER DEFAULT 0,  -- Seviye 1 Puanı
            seviye2 INTEGER DEFAULT 0,  -- Seviye 2 Puanı
            seviye3 INTEGER DEFAULT 0,  -- Seviye 3 Puanı
            toplam_puan INTEGER DEFAULT 0  -- Toplam Puan (Hesaplanmış)
        )
    ''')

    conn.commit()
    conn.close()

# Veritabanını oluştur
create_db()
