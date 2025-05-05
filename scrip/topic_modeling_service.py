from fastapi import FastAPI, HTTPException
import uvicorn
import os
import joblib
from scrip.topic_modeling import train_topic_model, evaluate_topic_model, load_data_from_csv

MODEL_PATH = "bertopic_model.pkl"
DATA_PATH = "csv/cleaned_titles.csv"

app = FastAPI(
    title="Topic Modeling Service API",
    description="API untuk training dan evaluasi topic modeling (BERTopic)",
    version="1.0.0"
)

@app.post("/train/", summary="Trigger Training Topic Modeling")
def train():
    try:
        texts = load_data_from_csv(DATA_PATH)
        model, topics, probs = train_topic_model(texts, model_path=MODEL_PATH)
        score = evaluate_topic_model(model, texts)
        return {"message": "Training selesai", "coherence_score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/topics/", summary="Lihat Topik Hasil Training")
def get_topics():
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=404, detail="Model belum dilatih.")
    model = joblib.load(MODEL_PATH)
    topics = model.get_topic_info().to_dict(orient="records")
    return {"topics": topics}

if __name__ == "__main__":
    uvicorn.run("topic_modeling_service:app", host="0.0.0.0", port=8004, reload=True)