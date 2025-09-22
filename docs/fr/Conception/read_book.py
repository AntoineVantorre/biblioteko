import os
import argparse
from google import genai
from dotenv import load_dotenv

load_dotenv() #charge les variable d env depuis .env

api_key = os.getenv("GEMINI_API_KEY") #recup la clef API

if not api_key:
    raise RunTimeError("pas de clef api reconnue")

def split_pdf(input_path, n=10, output_dir="parts"):
    os.makedirs(output_dir, exist_ok=True)
    reader = PyPDF2.PdrReader(input_path)
    for i in range(0, len(reader.pages), n):
        writer = PyPDF2.PdfWriter()
        for page in reader.pages[i:i+n]:
            writer.add_page(page)
        part_path = os.path.join(output_dir, f"part_{i//n+1}.pdf")
        with open(part_path, "wb") as f:
            writer.write(f)

client = genai.Client(api_key = api_key)

TEXTE_REQUETE = "extrait tout le texte du livre que je te join ici"

def generer_avec_fichier(chemin_fichier: str) -> str:
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            contenu fichier
    response = client.models.generate_content(model="gemini-1.5-flash")

print(reponse.text)

filepath = pathlib.Path('~tmp/sortie_read_book')