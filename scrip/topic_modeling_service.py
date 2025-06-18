# scrip/topic_modeling_service.py

from fastapi import FastAPI, HTTPException
import uvicorn
import logging
import os
import json # <-- Tambahkan import ini

# --- Import yang Diperlukan ---
# Kita butuh BERTopic untuk memuat model yang sudah disimpan
from bertopic import BERTopic

# Menggunakan impor relatif untuk memanggil fungsi pipeline utama
try:
    from .topic_modeling import run_topic_modeling_pipeline
except ImportError:
    run_topic_modeling_pipeline = None
    logging.error("Gagal mengimpor 'run_topic_modeling_pipeline' dari '.topic_modeling'. Pastikan file dan struktur direktori sudah benar.")

# --- Konfigurasi ---
MODEL_PATH = "bertopic_model.pkl"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Inisialisasi Aplikasi FastAPI ---
app = FastAPI(
    title="Topic Modeling Service",
    description="API untuk training dan inferensi model BERTopic.",
    version="1.0.0"
)


# --- Definisi Endpoint ---

@app.post("/train/", summary="Memicu Pipeline Topic Modeling")
def trigger_training_pipeline():
    """
    Endpoint ini akan memanggil satu fungsi `run_topic_modeling_pipeline`
    yang melakukan semuanya: memuat data, melatih model, mengevaluasi,
    dan menyimpan model yang sudah jadi.
    """
    if run_topic_modeling_pipeline is None:
        raise HTTPException(
            status_code=500,
            detail="Service tidak terkonfigurasi dengan benar karena gagal mengimpor fungsi pipeline."
        )

    try:
        logging.info("Permintaan training diterima. Memulai pipeline topic modeling...")
        
        # Panggil satu fungsi yang melakukan semua pekerjaan
        run_topic_modeling_pipeline()
        
        message = "Pipeline topic modeling berhasil diselesaikan."
        logging.info(message)
        return {"status": "success", "message": message, "model_path": MODEL_PATH}

    except Exception as e:
        logging.error(f"Terjadi error yang tidak terduga selama training: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Terjadi error internal: {e}")


@app.get("/topics/", summary="Mendapatkan Daftar Topik dari Model")
def get_trained_topics():
    """
    Endpoint ini akan memuat model BERTopic yang sudah disimpan dan
    mengembalikan informasi tentang topik-topik yang telah ditemukan.
    """
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=404, detail=f"Model tidak ditemukan di '{MODEL_PATH}'. Jalankan training terlebih dahulu.")
    
    try:
        logging.info(f"Memuat model dari {MODEL_PATH}...")
        
        trained_model = BERTopic.load(MODEL_PATH)
        
        logging.info("Model berhasil dimuat. Mengambil informasi topik...")
        
        topic_info = trained_model.get_topic_info()
        topic_info = topic_info[topic_info.Topic != -1]
        
        # --- PERBAIKAN DI SINI ---
        # Metode .to_json() dari pandas secara otomatis mengubah NaN menjadi null.
        # Kemudian kita muat kembali sebagai objek Python (list of dicts) yang sudah aman.
        # Ini adalah cara yang paling andal untuk menangani masalah ini.
        json_compatible_string = topic_info.to_json(orient="records")
        return json.loads(json_compatible_string)

    except Exception as e:
        logging.error(f"Gagal memuat atau memproses model: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Gagal memuat model. File mungkin rusak atau bukan model BERTopic. Error: {e}")


# --- Pemicu untuk Menjalankan Server ---
if __name__ == "__main__":
    uvicorn.run("scrip.topic_modeling_service:app", host="0.0.0.0", port=8004, reload=True)