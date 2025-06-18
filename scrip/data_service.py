# scrip/data_service.py

from fastapi import FastAPI, HTTPException
import uvicorn
import pandas as pd
import os
import json
import logging
from typing import List, Dict

# --- Import Model Loader ---
# Kita perlu BERTopic untuk memuat model yang sudah disimpan
try:
    from bertopic import BERTopic
except ImportError:
    BERTopic = None # Handle jika bertopic tidak terinstal
    logging.warning("Pustaka BERTopic tidak ditemukan. Endpoint /topics/ tidak akan berfungsi.")


# --- Konfigurasi ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Tentukan path absolut untuk folder csv dan model
# Ini memastikan path selalu benar, tidak peduli dari mana skrip dijalankan
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'csv', 'cleaned_titles.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'bertopic_model.pkl')


# --- Inisialisasi Aplikasi FastAPI ---
app = FastAPI(
    title="Data & Model Service API",
    description="API untuk menyajikan data bersih dan hasil topic modeling.",
    version="1.0.0"
)


# --- Definisi Endpoint ---

@app.get("/data/cleaned_titles",
         response_model=List[Dict[str, str]],
         summary="Mengambil Judul yang Sudah Dibersihkan")
def get_cleaned_titles():
    """
    Menyajikan daftar judul penelitian yang sudah dibersihkan dari file
    `cleaned_titles.csv`.
    """
    logging.info(f"Mencoba membaca data dari: {CSV_PATH}")
    if not os.path.exists(CSV_PATH):
        raise HTTPException(status_code=404, detail=f"File data bersih tidak ditemukan. Jalankan pipeline preprocessing terlebih dahulu.")

    try:
        df = pd.read_csv(CSV_PATH)
        if 'cleaned_title' not in df.columns:
            raise HTTPException(status_code=500, detail="Kolom 'cleaned_title' tidak ditemukan di CSV.")
        
        # Menggunakan .to_json() untuk menangani nilai NaN secara otomatis
        json_compatible_string = df[['Original Title', 'cleaned_title']].to_json(orient='records')
        return json.loads(json_compatible_string)

    except Exception as e:
        logging.error(f"Gagal memproses file CSV: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Gagal membaca atau memproses file data: {e}")


@app.get("/results/topics",
         summary="Mengambil Hasil Topic Modeling")
def get_model_topics():
    """
    Memuat model BERTopic yang sudah dilatih dan mengembalikan daftar topik
    yang telah ditemukan (mengabaikan topik outlier -1).
    """
    if BERTopic is None:
        raise HTTPException(status_code=501, detail="Fungsionalitas model tidak tersedia karena pustaka BERTopic tidak terinstal.")

    logging.info(f"Mencoba memuat model dari: {MODEL_PATH}")
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=404, detail=f"File model tidak ditemukan. Jalankan pipeline training terlebih dahulu.")

    try:
        # Gunakan BERTopic.load() untuk memuat model
        trained_model = BERTopic.load(MODEL_PATH)
        topic_info = trained_model.get_topic_info()
        
        # Mengabaikan topik outlier (-1) untuk output yang lebih bersih
        topic_info = topic_info[topic_info.Topic != -1]
        
        # Gunakan metode yang aman untuk JSON untuk menghindari error NaN
        json_compatible_string = topic_info.to_json(orient="records")
        return json.loads(json_compatible_string)

    except Exception as e:
        logging.error(f"Gagal memuat atau memproses model: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Gagal memuat atau menginterpretasi model: {e}")


# --- Pemicu untuk Menjalankan Server ---
if __name__ == "__main__":
    # PERBAIKAN: Beri tahu Uvicorn path lengkap ke objek 'app'
    uvicorn.run("scrip.data_service:app", host="0.0.0.0", port=8003, reload=True)