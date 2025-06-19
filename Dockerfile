# Langkah 1: Pilih Base Image
FROM python:3.11-slim

# Langkah 2: Atur Lingkungan
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# --- PERBAIKAN URUTAN DI SINI ---

# Langkah 3: Salin HANYA file requirements.txt terlebih dahulu
COPY requirements.txt .

# Langkah 4: Instal SEMUA dependensi dari requirements.txt
# Ini memastikan semua pustaka (nltk, pandas, dll.) sudah ada
# sebelum kode kita yang lain disalin.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Langkah 5: Salin sisa kode proyek Anda
# Sekarang kita salin folder scrip, csv, dll.
COPY . .

# Langkah 6: Jalankan skrip helper untuk mengunduh data NLTK
# Kali ini akan berhasil karena nltk sudah diinstal di Langkah 4.
RUN python scrip/download_helper.py

# Langkah 7: Buka port yang akan digunakan oleh service
EXPOSE 8001 8002 8003 8004

# Default command jika container dijalankan tanpa perintah khusus
CMD ["python"]