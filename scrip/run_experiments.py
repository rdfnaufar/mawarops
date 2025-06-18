# scrip/scraping.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os

# --- Konfigurasi ---
# Pindahkan semua variabel konfigurasi ke atas agar mudah diubah
CATEGORIES = [
    'cs.AI', 'cs.LG', 'cs.CL', 'cs.CV', 'cs.RO', 'cs.NE', 'cs.SI'
]
SHOW_PER_PAGE = 2000 
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
OUTPUT_DIR = 'csv'
OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, 'scraped_titles.csv')

# --- Fungsi Utama yang Bisa Diimpor ---
def run_scraping():
    """
    Fungsi ini membungkus seluruh logika scraping dari awal hingga akhir.
    Ini adalah fungsi yang akan dipanggil oleh run_experiments.py.
    """
    # Pastikan direktori output ada
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_titles = []
    all_authors = []

    print("Memulai proses scraping dengan metode /recent...")

    # Looping untuk setiap kategori dalam daftar CATEGORIES
    for category in CATEGORIES:
        url = f"https://arxiv.org/list/{category}/recent?show={SHOW_PER_PAGE}"
        print(f"\n--- Scraping Kategori: {category} ---")
        print(f"Mencoba URL: {url}")
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=20)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            current_titles = soup.find_all('div', class_='list-title', limit=SHOW_PER_PAGE)
            current_authors = soup.find_all('div', class_='list-authors', limit=SHOW_PER_PAGE)

            if not current_titles:
                print("    -> Info: Tidak ada judul yang ditemukan untuk kategori ini.")
                continue
            
            print(f"    -> Sukses! Menemukan {len(current_titles)} entri.")

            for title in current_titles:
                text = re.sub(r'(?i)^title[:\-\s]*', '', title.get_text(strip=True))
                all_titles.append(text)

            for author in current_authors:
                author_text = author.get_text(strip=True).replace("Authors:", "").strip()
                all_authors.append(author_text)
                
            time.sleep(3)

        except requests.exceptions.RequestException as e:
            print(f"    -> Gagal mengambil data untuk kategori {category}. Error: {e}")
            continue

    # --- Simpan ke CSV ---
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
        print("\nTidak ada data yang berhasil di-scrape.")

# --- Bagian untuk menjalankan file ini secara mandiri ---
# Ini tidak akan dieksekusi saat file diimpor oleh skrip lain.
if __name__ == '__main__':
    print("Menjalankan scraping.py secara langsung...")
    run_scraping()