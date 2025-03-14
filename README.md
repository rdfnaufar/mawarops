# mawarops

Sumber Data:
https://arxiv.org/list/cs.LG/recent

# Deskripsi Proyek
Proyek ini bertujuan untuk melakukan web scraping terhadap judul-judul penelitian, membersihkan data menggunakan Natural Language Processing (NLP) dengan NLTK, dan menyimpannya dalam format CSV.

# Teknologi yang Digunakan
Python: Bahasa pemrograman utama
Requests: Mengambil data dari website
BeautifulSoup: Parsing HTML untuk mengekstrak data
Pandas: Pengolahan dan penyimpanan data dalam format CSV
NLTK: Pembersihan teks dengan NLP

## Struktur File
- **repository/**
  - `scraping.ipynb` 
  - `README.md` 
  - `scraped_titles.csv`
  - `bert_embeddings.csv`
  - `cleaned_titles.csv`
  - `preprocessing.py`
  - `scraping.py`


# Instalasi dan Penggunaan
1. Clone Repository
2. Instalasi Dependensi
3. Jalankan Script

# Cara Kerja Script
## 1. Mengambil Data
- Menggunakan requests untuk mengambil HTML dari halaman arXiv.
- Menggunakan BeautifulSoup untuk mengekstrak judul penelitian dari halaman tersebut.
## 2. Membersihkan Data
- Menggunakan NLTK untuk tokenisasi, stopword removal, dan lemmatization.
- Menghapus karakter yang tidak relevan dengan penelitian.
## 3. Menyimpan Data
- Data asli dan hasil pembersihan disimpan dalam file scraped_titles.csv.

# Catatan Penting
- Pastikan koneksi internet stabil saat menjalankan script.
- Jika terdapat error saat scraping, coba ubah User-Agent di headers agar menyerupai browser yang berbeda.
