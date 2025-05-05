import pandas as pd
from fastapi import FastAPI, HTTPException
import uvicorn
import os
from typing import List, Dict # Untuk type hinting respons

# Tentukan path absolut untuk folder csv (sama seperti di scraping_service)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Menunjuk ke 'mawarops'
CSV_FOLDER = os.path.join(BASE_DIR, 'csv')
CLEANED_CSV_PATH = os.path.join(CSV_FOLDER, 'cleaned_titles.csv')
# Jika ingin menampilkan embedding juga nanti:
# BERT_CSV_PATH = os.path.join(CSV_FOLDER, 'bert_embeddings.csv')

app = FastAPI(
    title="Processed Data Service API",
    description="API untuk mengambil data judul yang sudah dipreproses.",
    version="1.0.0"
)

@app.get("/titles/cleaned/",
         response_model=List[Dict[str, str]], # Menentukan struktur respons (list of dictionaries)
         summary="Ambil Judul Bersih",
         description="Mengembalikan daftar judul penelitian yang sudah dibersihkan dari file cleaned_titles.csv.")
async def get_cleaned_titles():
    """
    Endpoint untuk mengambil semua data dari cleaned_titles.csv.
    """
    if not os.path.exists(CLEANED_CSV_PATH):
        raise HTTPException(status_code=404, detail=f"File '{os.path.basename(CLEANED_CSV_PATH)}' tidak ditemukan. Jalankan preprocessing terlebih dahulu.")

    try:
        df = pd.read_csv(CLEANED_CSV_PATH)
        # Konversi DataFrame ke format list of dictionaries (JSON serializable)
        # Hanya ambil kolom 'Original Title' dan 'Cleaned Title' untuk contoh ini
        if 'Original Title' not in df.columns or 'Cleaned Title' not in df.columns:
             raise HTTPException(status_code=500, detail="Kolom 'Original Title' atau 'Cleaned Title' tidak ditemukan di CSV.")

        results = df[['Original Title', 'Cleaned Title']].to_dict(orient='records')
        return results
    except pd.errors.EmptyDataError:
        # Tangani jika file CSV kosong
         raise HTTPException(status_code=404, detail=f"File '{os.path.basename(CLEANED_CSV_PATH)}' kosong.")
    except Exception as e:
        print(f"Error saat membaca atau memproses CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Gagal membaca atau memproses file CSV: {e}")

# Perintah untuk menjalankan server (jika file ini dijalankan langsung)
if __name__ == "__main__":
    # Jalankan di port yang berbeda, misal 8002
    uvicorn.run("data_service:app", host="0.0.0.0", port=8003, reload=True)