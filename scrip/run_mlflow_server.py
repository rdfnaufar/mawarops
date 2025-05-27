import os
import subprocess

# Direktori untuk menyimpan MLflow artifacts
os.makedirs("mlruns", exist_ok=True)

# Jalankan MLflow server
print("Starting MLflow server...")
subprocess.run(["mlflow", "ui", "--port", "5000"])