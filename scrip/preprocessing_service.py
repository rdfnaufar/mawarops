from fastapi import FastAPI, HTTPException
import pandas as pd
import uvicorn
import os
from scrip.preprocessing import clean_text
import nltk

app = FastAPI(
    title="Preprocessing Service API",
    description="API untuk preprocessing data judul penelitian.",
    version="1.0.0"
)

CSV_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv')
SCRAPED_PATH = os.path.join(CSV_FOLDER, 'scraped_titles.csv')
CLEANED_PATH = os.path.join(CSV_FOLDER, 'cleaned_titles.csv')

@app.post("/preprocess/", summary="Preprocessing Judul")
def preprocess_titles():
    try:
        df = pd.read_csv(SCRAPED_PATH)
        if 'Original Title' not in df.columns:
            raise HTTPException(status_code=400, detail="Kolom 'Original Title' tidak ditemukan.")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        df['Cleaned Title'] = df['Original Title'].apply(clean_text)
        df.to_csv(CLEANED_PATH, index=False, encoding='utf-8')
        return {"message": f"Preprocessing selesai! File disimpan sebagai {CLEANED_PATH}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("preprocessing_service:app", host="0.0.0.0", port=8002, reload=True)