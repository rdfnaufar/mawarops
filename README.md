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

# Instalasi dan Penggunaan
1. Clone Repository
2. Instalasi Dependensi
3. Jalankan Script

# Cara Kerja Script
## Mengambil Data
Menggunakan requests untuk mengambil HTML dari halaman arXiv.
Menggunakan BeautifulSoup untuk mengekstrak judul penelitian dari halaman tersebut.
## Membersihkan Data
Menggunakan NLTK untuk tokenisasi, stopword removal, dan lemmatization.
Menghapus karakter yang tidak relevan dengan penelitian.
## Menyimpan Data
Data asli dan hasil pembersihan disimpan dalam file scraped_titles.csv.

# Catatan Penting
Pastikan koneksi internet stabil saat menjalankan script.
Jika terdapat error saat scraping, coba ubah User-Agent di headers agar menyerupai browser yang berbeda.
