import os
import wandb
import multiprocessing
from topic_modeling import train_topic_model, evaluate_topic_model, load_data_from_csv

def run_experiment_with_wandb(csv_path):
    """
    Jalankan eksperimen topic modeling dengan W&B tracking
    """
    # Inisialisasi W&B
    wandb.init(project="topic-modeling-comparison", name="bertopic-experiment")
    
    # Load data
    texts = load_data_from_csv(csv_path)
    
    # Log parameter
    wandb.log({"num_samples": len(texts)})
    
    # Train model menggunakan kode yang sudah ada
    model_path = "bertopic_model_wandb.pkl"
    model, topics, probs = train_topic_model(texts, model_path=model_path)
    
    # Log model sebagai artifact
    wandb.save(model_path)
    
    # Visualisasi topik (jika tersedia)
    try:
        fig = model.visualize_topics()
        fig_path = "topic_visualization_wandb.html"
        fig.write_html(fig_path)
        wandb.save(fig_path)
    except Exception as e:
        print(f"Tidak bisa membuat visualisasi: {e}")
    
    # Log metrics
    try:
        # Hitung coherence score
        coherence_score = evaluate_topic_model(model, texts)
        wandb.log({"coherence_score": coherence_score})
    except Exception as e:
        print(f"Tidak bisa menghitung coherence score: {e}")
    
    # Log jumlah topik
    wandb.log({"num_topics": len(model.get_topics())})
    
    # Finish W&B run
    wandb.finish()
    
    return model, topics, probs

if __name__ == "__main__":
    # Penting untuk Windows
    multiprocessing.freeze_support()
    
    # Login ke W&B
    wandb.login()
    
    # Path ke file CSV
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'cleaned_titles.csv')
    
    # Jalankan eksperimen dengan W&B tracking
    print("Menjalankan eksperimen dengan W&B tracking...")
    model, topics, probs = run_experiment_with_wandb(csv_path)
    
    print("Eksperimen selesai. Cek W&B dashboard untuk hasil.")