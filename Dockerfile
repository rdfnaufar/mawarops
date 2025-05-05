FROM python:3.10-slim

WORKDIR /workspaces/mawarops

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001 8002 8003 8004

CMD ["uvicorn", "scrip.scraping_service:app", "--host", "0.0.0.0", "--port", "8001"]