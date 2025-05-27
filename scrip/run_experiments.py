import os
import mlflow
import multiprocessing
from topic_modeling import train_topic_model, evaluate_topic_model, load_data_from_csv

def run_experiment_with_mlflow(csv_path, experiment_name="Topic_Modeling"):
    """
    Jalankan eksperimen topic modeling dengan MLflow tracking
    """
    # Setup MLflow
    mlflow.set_experiment(experiment_name)
    
    # Load data
    texts = load_data_from_csv(csv_path)
    
    # Mulai MLflow run
    with mlflow.start_run():
        # Log parameter
        mlflow.log_param("num_samples", len(texts))
        
        # Train model menggunakan kode yang sudah ada
        model_path = "bertopic_model.pkl"
        model, topics, probs = train_topic_model(texts, model_path=model_path)
        
        # Log model sebagai artifact
        mlflow.log_artifact(model_path)
        
        # Visualisasi topik (jika tersedia)
        try:
            fig = model.visualize_topics()
            fig_path = "topic_visualization.html"
            fig.write_html(fig_path)
            mlflow.log_artifact(fig_path)
        except Exception as e:
            print(f"Tidak bisa membuat visualisasi: {e}")
        
        # Log metrics
        try:
            # Hitung coherence score
            coherence_score = evaluate_topic_model(model, texts)
            mlflow.log_metric("coherence_score", coherence_score)
        except Exception as e:
            print(f"Tidak bisa menghitung coherence score: {e}")
        
        # Log jumlah topik
        mlflow.log_metric("num_topics", len(model.get_topics()))
        
    return model, topics, probs

if __name__ == "__main__":
    # Penting untuk Windows
    multiprocessing.freeze_support()
    
    # Path ke file CSV
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'cleaned_titles.csv')
    
    # Jalankan eksperimen dengan MLflow tracking
    print("Menjalankan eksperimen dengan MLflow tracking...")
    model, topics, probs = run_experiment_with_mlflow(csv_path)
    
    print("Eksperimen selesai. Cek MLflow UI untuk hasil.")