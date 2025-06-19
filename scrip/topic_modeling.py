# scrip/topic_modeling.py

import pandas as pd
from bertopic import BERTopic
from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel
import os
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

# --- Konfigurasi ---
INPUT_FILENAME = 'csv/cleaned_titles.csv'
MODEL_FILENAME = 'bertopic_model.pkl' # Nama file untuk menyimpan model

# --- Fungsi-fungsi (sedikit disempurnakan) ---

def train_topic_model(texts, model_path):
    """
    Latih model BERTopic pada list teks dan simpan hasilnya.
    """
    print(f"Memulai training BERTopic dengan {len(texts)} dokumen...")
    
    # Inisialisasi BERTopic dengan beberapa parameter yang direkomendasikan
    # language='english' penting untuk stopwords internal model
    # calculate_probabilities=True dibutuhkan untuk beberapa visualisasi
    # verbose=True akan menampilkan progress bar saat training
    topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True)

    # Latih model. Ini mungkin memakan waktu beberapa menit.
    topics, probs = topic_model.fit_transform(texts)
    
    print("Pelatihan model selesai.")

    # Simpan model menggunakan metode bawaan BERTopic (lebih baik dari joblib)
    # serialization="safetensors" lebih modern dan aman
    topic_model.save(model_path, serialization="safetensors")
    print(f"Model BERTopic berhasil disimpan di {model_path}")

    return topic_model

def evaluate_topic_model(model, texts):
    """
    Hitung coherence score (c_v) untuk model BERTopic menggunakan Gensim.
    """
    print("\nMemulai evaluasi model dengan Coherence Score (c_v)...")
    
    # Ambil topik dari BERTopic. Kita perlu mengabaikan topik outlier (-1).
    bertopic_topics = []
    for topic_id in sorted(model.get_topics()):
        if topic_id == -1:  # Abaikan topik outlier
            continue
        words = [word for word, _ in model.get_topic(topic_id)]
        bertopic_topics.append(words)

    # Preprocessing untuk Gensim (tokenisasi sederhana)
    tokenized_texts = [text.split() for text in texts]

    # Buat dictionary dan corpus
    dictionary = Dictionary(tokenized_texts)
    corpus = [dictionary.doc2bow(text) for text in tokenized_texts]

    # Hitung coherence
    coherence_model = CoherenceModel(
        topics=bertopic_topics,
        texts=tokenized_texts,
        dictionary=dictionary,
        coherence='c_v'
    )
    coherence_score = coherence_model.get_coherence()
    
    print(f"--> Coherence Score (c_v): {coherence_score:.4f}")
    return coherence_score

def load_data_from_csv(csv_path):
    """
    Load dan ambil teks dari file CSV hasil preprocessing.
    """
    print(f"Membaca data bersih dari: {csv_path}")
    if not os.path.exists(csv_path):
        # ... (error handling)
        return None

    df = pd.read_csv(csv_path)
    
    # --- TAMBAHKAN BARIS INI ---
    # Ambil hanya 500 baris pertama untuk meringankan beban
    df = df.head(500) 
    print("INFO: Hanya menggunakan 500 baris pertama dari data untuk meringankan proses.")
    # ---------------------------

    # ... (sisa fungsi sama)
    return df['cleaned_title'].dropna().tolist()

# --- BAGIAN UTAMA UNTUK MENJALANKAN SEMUANYA ---
if __name__ == '__main__':
    # Langkah 1: Muat data yang sudah bersih
    texts_to_model = load_data_from_csv(INPUT_FILENAME)
    
    # Hanya lanjutkan jika data berhasil dimuat
    if texts_to_model:
        # Langkah 2: Latih model
        trained_model = train_topic_model(texts_to_model, MODEL_FILENAME)
        
        # Langkah 3: Evaluasi model yang baru saja dilatih
        evaluate_topic_model(trained_model, texts_to_model)
        
        # Langkah 4: Tampilkan beberapa informasi dasar tentang topik
        print("\nInformasi Topik (10 Teratas):")
        # Menampilkan topik-topik utama yang ditemukan oleh model
        print(trained_model.get_topic_info().head(11))