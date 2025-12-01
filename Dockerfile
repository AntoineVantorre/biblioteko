FROM python:3.9-slim

WORKDIR /app/src

# Copier tout le répertoire src dans l'image
COPY src/ /app/src/

# Installer les dépendances (chemin vers requirements dans src/app)
RUN pip install --no-cache-dir -r /app/src/app/requirements.txt

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
