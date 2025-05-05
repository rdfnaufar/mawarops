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

# Microservices & Workflow

Proyek ini terdiri dari beberapa service terpisah (microservices) yang saling terintegrasi untuk scraping, preprocessing, dan topic modeling:

- **scraping_service** (port 8001): Melakukan scraping judul dan author dari arXiv, hasil disimpan ke `csv/scraped_titles.csv`.
- **preprocessing_service** (port 8002): Melakukan preprocessing data hasil scraping, hasil disimpan ke `csv/cleaned_titles.csv`.
- **data_service** (port 8003): Menyediakan endpoint untuk mengambil data yang sudah dipreproses.
- **topic_modeling_service** (port 8004): Melatih dan mengevaluasi model topic modeling (BERTopic) serta menyediakan endpoint untuk melihat hasil topik.

## Alur Kerja

1. **Scraping**: Jalankan endpoint `/scrape/` pada port 8001 untuk mengambil data dari arXiv.
2. **Preprocessing**: Jalankan endpoint `/preprocess/` pada port 8002 untuk membersihkan data hasil scraping.
3. **Topic Modeling**: Jalankan endpoint `/train/` pada port 8004 untuk melatih model topic modeling dan menghitung coherence score.
4. **Lihat Topik**: Endpoint `/topics/` pada port 8004 dapat digunakan untuk melihat hasil topik yang telah diidentifikasi oleh model.

## API Endpoints

- **POST /scrape/** (8001): Memicu proses scraping data dari arXiv.
- **POST /preprocess/** (8002): Memicu proses preprocessing data hasil scraping.
- **GET /titles/cleaned/** (8003): Mendapatkan daftar judul yang sudah dibersihkan.
- **POST /train/** (8004): Melatih model topic modeling dan menghitung coherence score menggunakan Gensim.
- **GET /topics/** (8004): Mendapatkan daftar topik hasil training model.

## Catatan

- Semua proses utama dapat diakses melalui API, sehingga workflow dapat diotomatisasi sepenuhnya.
- Coherence score pada topic modeling dihitung menggunakan Gensim untuk memastikan evaluasi model yang sesuai standar.

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
