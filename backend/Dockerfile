FROM python:3.11

WORKDIR /app

# Installer FastAPI & Uvicorn
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier tout le backend
COPY . .

# Copier le dist généré par le service frontend
# (le dist sera monté comme volume par docker-compose)
COPY ./dist ./static/dist

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
