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
FastAPI: Membuat REST API untuk akses data
Docker: Containerisasi aplikasi untuk deployment yang konsisten

## Struktur File
- **repository/**
  - `|csv`  
    - `cleaned_titles.csv`
    - `|-scraped_titles.csv`
    - `|-bert_embeddings.csv`
  - `|scrip`
    - `|-visualization.ipynb` 
    - `|-preprocessing.py`
    - `|-scraping.py`
    - `|-scraping_service.py`
    - `|-data_service.py`
  - `Dockerfile`
  - `docker-compose.yml`
  - `|README.md` 


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

# API Endpoints
- **POST /scrape/**: Memicu proses scraping data dari arXiv
- **GET /titles/cleaned/**: Mendapatkan daftar judul yang sudah dibersihkan

# Cara Menjalankan dengan Docker
1. Pastikan Docker sudah terinstal
2. Jalankan perintah: `docker compose up --build`
3. Akses API di:
   - http://localhost:8001/scrape/ (POST untuk scraping)
   - http://localhost:8002/titles/cleaned/ (GET untuk data yang sudah diproses)

# Catatan Penting
- Pastikan koneksi internet stabil saat menjalankan script.
- Jika terdapat error saat scraping, coba ubah User-Agent di headers agar menyerupai browser yang berbeda.
