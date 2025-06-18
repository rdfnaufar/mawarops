# scrip/preprocessing_service.py

from fastapi import FastAPI, HTTPException
import uvicorn
import logging
import os

# --- Import fungsi utama dari file logika ---
# Menggunakan impor relatif dengan tanda titik (.)
try:
    from .preprocessing import run_preprocessing
except ImportError:
    run_preprocessing = None
    logging.error("Gagal mengimpor 'run_preprocessing' dari '.preprocessing'. Pastikan file dan struktur direktori sudah benar.")


# --- Konfigurasi Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# --- Inisialisasi Aplikasi FastAPI ---
app = FastAPI(
    title="Preprocessing Service",
    description="API untuk memicu proses preprocessing data judul penelitian.",
    version="1.0.0"
)


# --- Definisi Endpoint ---
@app.post("/preprocess/", summary="Memicu Proses Preprocessing")
def trigger_preprocessing_task():
    """
    Endpoint ini akan memanggil fungsi `run_preprocessing` yang berisi
    seluruh logika untuk membaca, membersihkan, dan menyimpan data.
    """
    if run_preprocessing is None:
        raise HTTPException(
            status_code=500, 
            detail="Service tidak terkonfigurasi dengan benar karena gagal mengimpor fungsi preprocessing."
        )

    try:
        logging.info("Permintaan preprocessing diterima. Memulai proses...")
        run_preprocessing()
        message = "Proses preprocessing berhasil diselesaikan."
        logging.info(message)
        return {"status": "success", "message": message}

    except FileNotFoundError as e:
        logging.error(f"File input tidak ditemukan: {e}")
        raise HTTPException(status_code=404, detail=f"File input tidak ditemukan. Pastikan 'scraped_titles.csv' ada. Detail: {e}")
    
    except Exception as e:
        logging.error(f"Terjadi error yang tidak terduga selama preprocessing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Terjadi error internal: {e}")


# --- Pemicu untuk Menjalankan Server ---
if __name__ == "__main__":
    # --- PERBAIKAN DI SINI ---
    # Beri tahu Uvicorn path lengkap ke objek 'app'
    # yaitu: paket.modul:objek
    uvicorn.run("scrip.preprocessing_service:app", host="0.0.0.0", port=8002, reload=True)