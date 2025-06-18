# scrip/scraping_service.py

from fastapi import FastAPI, HTTPException
import uvicorn
import logging

# --- Import fungsi utama dari file logika ---
# Menggunakan impor relatif (.) untuk memanggil dari direktori yang sama.
# Ini mengasumsikan Anda memiliki file 'scraping.py' dengan fungsi 'run_scraping()'.
try:
    from .scraping import run_scraping
except ImportError:
    run_scraping = None
    logging.error("Gagal mengimpor 'run_scraping' dari '.scraping'. Pastikan file dan struktur direktori sudah benar.")


# --- Konfigurasi Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# --- Inisialisasi Aplikasi FastAPI ---
app = FastAPI(
    title="Scraping Service",
    description="API untuk memicu proses scraping multi-kategori dari arXiv.",
    version="1.0.0"
)


# --- Definisi Endpoint ---
@app.post("/scrape/", summary="Memicu Proses Scraping arXiv")
def trigger_scraping_task():
    """
    Endpoint ini akan memanggil fungsi `run_scraping` dari file `scraping.py`.
    Fungsi tersebut berisi logika untuk mengambil data dari berbagai kategori
    dan menyimpannya ke 'scraped_titles.csv'.
    """
    if run_scraping is None:
        raise HTTPException(
            status_code=500, 
            detail="Service tidak terkonfigurasi dengan benar karena gagal mengimpor fungsi scraping."
        )

    try:
        logging.info("Permintaan scraping diterima. Memulai proses...")
        
        # Panggil satu fungsi yang melakukan semua pekerjaan berat
        run_scraping()
        
        message = "Proses scraping berhasil diselesaikan."
        logging.info(message)
        return {"status": "success", "message": message}

    except Exception as e:
        # Menangkap semua error lain yang mungkin terjadi selama scraping
        logging.error(f"Terjadi error yang tidak terduga selama scraping: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Terjadi error internal: {e}")


# --- Pemicu untuk Menjalankan Server ---
if __name__ == "__main__":
    # PERBAIKAN: Beri tahu Uvicorn path lengkap ke objek 'app'
    # yaitu: paket.modul:objek
    # Ini memungkinkan Anda menjalankan server dengan benar dari direktori utama.
    uvicorn.run("scrip.scraping_service:app", host="0.0.0.0", port=8001, reload=True)