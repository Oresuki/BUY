from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_diamond_lock_price():
    url = 'https://gtid.site/'  # URL target
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Cari elemen harga di situs target (ganti selector sesuai situs)
        harga_element = soup.find('span', class_='price')  # Sesuaikan selector
        if harga_element:
            harga = harga_element.text.strip().replace('Rp', '').replace(',', '').strip()
            return int(harga)  # Konversi ke angka
        else:
            return None
    except Exception as e:
        print(f"Error saat scraping: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')  # File HTML yang akan ditampilkan

@app.route('/api/harga-dl', methods=['GET'])
def get_harga_dl():
    harga = scrape_diamond_lock_price()
    if harga:
        return jsonify({'harga': harga})
    else:
        return jsonify({'error': 'Gagal mengambil harga'}), 500

if __name__ == '__main__':
    app.run(debug=True)
