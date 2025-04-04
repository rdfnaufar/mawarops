FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pastikan folder csv ada
RUN mkdir -p csv

# Expose port untuk kedua service
EXPOSE 8001
EXPOSE 8002

# Jalankan kedua service
CMD ["sh", "-c", "python scrip/scraping_service.py & python scrip/data_service.py"]