import nltk
import os
import ssl

# Trik untuk mengatasi masalah sertifikat SSL yang sering terjadi di Windows
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Tentukan direktori target di dalam folder proyek saat ini
DOWNLOAD_DIR = 'nltk_data'

# Buat direktori jika belum ada
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)
    print(f"Direktori '{DOWNLOAD_DIR}' dibuat.")

# Daftar paket yang dibutuhkan oleh proyek Anda
packages = ['punkt', 'stopwords', 'wordnet', 'omw-1.4']

print(f"Memulai proses unduh manual data NLTK ke ./{DOWNLOAD_DIR}...")

for package_id in packages:
    try:
        print(f"--> Mengunduh '{package_id}'...")
        # Menentukan direktori unduhan secara eksplisit
        nltk.download(package_id, download_dir=DOWNLOAD_DIR)
        print(f"    '{package_id}' berhasil diunduh ke '{DOWNLOAD_DIR}'.")
    except Exception as e:
        print(f"    Gagal mengunduh '{package_id}'. Error: {e}")

print("\nProses unduh manual selesai.")