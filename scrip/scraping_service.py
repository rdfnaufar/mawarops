import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from fastapi import FastAPI, HTTPException
import uvicorn
import os

# Tentukan path absolut untuk folder csv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Ini akan menunjuk ke folder 'mawarops'
CSV_FOLDER = os.path.join(BASE_DIR, 'csv')
CSV_PATH = os.path.join(CSV_FOLDER, 'scraped_titles.csv')

# Pastikan folder csv ada
os.makedirs(CSV_FOLDER, exist_ok=True)

app = FastAPI(
    title="Scraping Service API",
    description="API untuk melakukan scraping judul penelitian dari arXiv.",
    version="1.0.0"
)

def perform_scraping():
    """Fungsi inti untuk melakukan scraping."""
    URL = "https://arxiv.org/list/cs.LG/recent"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"} # Contoh User-Agent

    try:
        response = requests.get(URL, headers=headers, timeout=30) # Tambahkan timeout
        response.raise_for_status() # Cek jika ada HTTP error (misal: 404, 500)
    except requests.exceptions.RequestException as e:
        print(f"Error saat request ke {URL}: {e}")
        raise HTTPException(status_code=503, detail=f"Gagal mengambil data dari arXiv: {e}")

    soup = BeautifulSoup(response.text, 'html.parser')

    titles = []
    authors = []

    # Scraping Judul
    title_elements = soup.find_all('div', class_='list-title mathjax')
    if not title_elements:
         raise HTTPException(status_code=500, detail="Tidak dapat menemukan elemen judul di halaman arXiv. Struktur halaman mungkin berubah.")

    for title in title_elements:
        # Hapus 'Title:' dan spasi ekstra
        text = title.get_text(strip=True).replace("Title:", "").strip()
        titles.append(text)

    # Scraping Author
    author_elements = soup.find_all('div', class_='list-authors')
    if not author_elements:
         raise HTTPException(status_code=500, detail="Tidak dapat menemukan elemen author di halaman arXiv. Struktur halaman mungkin berubah.")

    for author in author_elements:
        author_text = author.get_text(strip=True).replace("Authors:", "").strip()
        authors.append(author_text)

    if not titles or not authors or len(titles) != len(authors):
        raise HTTPException(status_code=500, detail=f"Jumlah judul ({len(titles)}) dan author ({len(authors)}) tidak cocok atau kosong setelah scraping.")

    try:
        df = pd.DataFrame({'Original Title': titles, 'Authors': authors})
        df.to_csv(CSV_PATH, index=False, encoding='utf-8')
        return {"message": f"Scraping berhasil! {len(titles)} judul disimpan ke {CSV_PATH}"}
    except Exception as e:
        print(f"Error saat menyimpan ke CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan data ke CSV: {e}")

@app.post("/scrape/", summary="Memicu Proses Scraping", description="Menjalankan proses scraping data judul dan author dari arXiv dan menyimpannya ke file CSV.")
async def trigger_scraping():
    """
    Endpoint untuk memulai proses scraping.
    Akan mengembalikan pesan sukses atau error jika terjadi masalah.
    """
    try:
        result = perform_scraping()
        return result
    except HTTPException as http_exc:
        # Langsung teruskan HTTPException yang sudah dibuat di perform_scraping
        raise http_exc
    except Exception as e:
        # Tangani error tak terduga lainnya
        print(f"Error tidak terduga saat scraping: {e}")
        raise HTTPException(status_code=500, detail=f"Terjadi error internal: {e}")

# Perintah untuk menjalankan server (jika file ini dijalankan langsung)
if __name__ == "__main__":
    # host="0.0.0.0" agar bisa diakses dari luar container nantinya
    # reload=True bagus untuk development, otomatis restart saat kode berubah
    uvicorn.run("scraping_service:app", host="0.0.0.0", port=8001, reload=True)