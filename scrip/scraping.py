import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os

# --- Konfigurasi ---
# Daftar kategori yang diinginkan untuk membuat pencarian lebih general
CATEGORIES = [
    'cs.AI',  # Artificial Intelligence
    'cs.LG',  # Machine Learning
    'cs.CL',  # Computation and Language (NLP)
    'cs.CV',  # Computer Vision and Pattern Recognition
    'cs.RO',  # Robotics
    'cs.NE',  # Neural and Evolutionary Computing
    'cs.SI'   # Social and Information Networks
]
# Anda bisa menambah atau mengurangi kategori dari daftar di atas
# Daftar lengkap bisa dilihat di: https://arxiv.org/archive/cs

# Jumlah entri maksimum untuk diambil dari halaman "recent" setiap kategori
# arXiv mengizinkan hingga 2000
SHOW_PER_PAGE = 2000 

# Header untuk request
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
# Direktori output
OUTPUT_DIR = 'csv'
OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, 'scraped_titles.csv')

# Pastikan direktori output ada
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Proses Scraping Utama ---
all_titles = []
all_authors = []

print("Memulai proses scraping dengan metode /recent...")

# Looping untuk setiap kategori dalam daftar CATEGORIES
for category in CATEGORIES:
    # Membuat URL target dengan parameter show
    url = f"https://arxiv.org/list/{category}/recent?show={SHOW_PER_PAGE}"
    
    print(f"\n--- Scraping Kategori: {category} ---")
    print(f"Mencoba URL: {url}")
    
    try:
        # Mengirim request ke URL
        response = requests.get(url, headers=HEADERS, timeout=20) # Timeout lebih lama untuk request besar
        response.raise_for_status() # Akan error jika status code bukan 2xx

        # Parsing HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Mencari semua judul dan penulis di halaman
        # Menggunakan 'limit' untuk memastikan tidak mengambil lebih dari yang diminta
        current_titles = soup.find_all('div', class_='list-title', limit=SHOW_PER_PAGE)
        current_authors = soup.find_all('div', class_='list-authors', limit=SHOW_PER_PAGE)

        if not current_titles:
            print("    -> Info: Tidak ada judul yang ditemukan untuk kategori ini.")
            continue
            
        print(f"    -> Sukses! Menemukan {len(current_titles)} entri.")

        # Ekstraksi Teks Judul
        for title in current_titles:
            text = re.sub(r'(?i)^title[:\-\s]*', '', title.get_text(strip=True))
            all_titles.append(text)

        # Ekstraksi Teks Author
        for author in current_authors:
            author_text = author.get_text(strip=True).replace("Authors:", "").strip()
            all_authors.append(author_text)
            
        # Jeda antar request agar sopan dan tidak di-block oleh server
        time.sleep(3)

    except requests.exceptions.RequestException as e:
        print(f"    -> Gagal mengambil data untuk kategori {category}. Error: {e}")
        continue

# --- Simpan ke CSV ---
# Menghapus duplikat data jika ada paper yang masuk ke beberapa kategori
min_length = min(len(all_titles), len(all_authors))
df = pd.DataFrame({
    'Original Title': all_titles[:min_length],
    'Authors': all_authors[:min_length]
})

print(f"\nTotal data sebelum menghapus duplikat: {len(df)}")
df.drop_duplicates(subset=['Original Title'], inplace=True)
print(f"Total data setelah menghapus duplikat: {len(df)}")


if not df.empty:
    df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8')
    print(f"\nScraping selesai! Total {len(df)} data unik disimpan ke {OUTPUT_FILENAME}")
else:
    print("\nTidak ada data yang berhasil di-scrape. Periksa kembali output error di atas.")