import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os

# --- Pengaturan Path NLTK ---
# Tambahkan path lokal ke daftar pencarian NLTK.
NLTK_DATA_PATH = 'nltk_data'
if os.path.exists(NLTK_DATA_PATH):
    nltk.data.path.append(NLTK_DATA_PATH)
else:
    print("="*60)
    print(f"ERROR: Direktori '{NLTK_DATA_PATH}' tidak ditemukan!")
    print("Pastikan Anda sudah menjalankan 'python scrip/download_helper.py' terlebih dahulu.")
    print("="*60)
    exit()

# --- Konfigurasi ---
INPUT_FILENAME = 'csv/scraped_titles.csv'
OUTPUT_FILENAME = 'csv/cleaned_titles.csv'

# --- Inisialisasi Alat ---
try:
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
except LookupError as e:
    print("="*60)
    print(f"ERROR: Gagal memuat resource NLTK. Error: {e}")
    print(f"Meskipun direktori '{NLTK_DATA_PATH}' ada, resource di dalamnya mungkin rusak.")
    print("Coba hapus folder 'nltk_data' dan jalankan kembali 'download_helper.py'.")
    print("="*60)
    exit() 

# --- FUNGSI CLEAN_TEXT (VERSI BARU) ---
def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    
    # --- PERUBAHAN UTAMA DI SINI ---
    # Kita tidak lagi menggunakan nltk.word_tokenize() yang bermasalah.
    # Kita gunakan .split() standar dari Python, yang aman karena tanda baca sudah hilang.
    tokens = text.split()
    
    cleaned_tokens = [
        lemmatizer.lemmatize(word) for word in tokens 
        if word not in stop_words and len(word) > 2
    ]
    return ' '.join(cleaned_tokens)

def run_preprocessing():
    print(f"Membaca data mentah dari: {INPUT_FILENAME}")
    if not os.path.exists(INPUT_FILENAME):
        print(f"Error: File '{INPUT_FILENAME}' tidak ditemukan.")
        return

    df = pd.read_csv(INPUT_FILENAME)
    if 'Original Title' not in df.columns:
        print("Error: Kolom 'Original Title' tidak ditemukan.")
        return
        
    print("Memulai proses pembersihan teks...")
    df['cleaned_title'] = df['Original Title'].apply(clean_text)
    df.dropna(subset=['cleaned_title'], inplace=True)
    df = df[df['cleaned_title'].str.strip() != '']

    print(f"Pembersihan selesai. Menyimpan hasil ke: {OUTPUT_FILENAME}")
    df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8')
    print(f"Proses preprocessing berhasil diselesaikan.")

if __name__ == '__main__':
    run_preprocessing()