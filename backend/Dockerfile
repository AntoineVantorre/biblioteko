FROM python:3.11

WORKDIR /app

# Install system deps required by some Python packages (OpenCV needs libGL)
RUN apt-get update && apt-get install -y --no-install-recommends \
	libgl1 \
	libglib2.0-0 \
	poppler-utils \
	libsm6 \
	libxrender1 \
	libxext6 \
 && rm -rf /var/lib/apt/lists/*

# Installer FastAPI & Uvicorn
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier tout le backend
COPY . .

# Copier le dist généré par le service frontend
# (le dist sera monté comme volume par docker-compose)
COPY ./dist ./static/dist

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
