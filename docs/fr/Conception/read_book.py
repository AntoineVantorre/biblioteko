import os
import argparse
import pathlib
from google import genai
import PyPDF2

with open('./apikey', 'r') as fichier:
     apikey = fichier.read()

filepath = pathfile.Path('./tmp/sortie.pdf')

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

split_pdf('../../../Dowloads/QueSaisJe_1_LesÉtapesDeLaBiologie_1954_7_MauriceCaullery.pdf')

client = genai.Client(api_key = api_key)

for file in sorted(Path("parts").iterdir(), key=lambda f: int(''.join(filter("aide moi ici")))):
     if file.is_file():
          print('converting file: ' + file.name)
          


TEXTE_REQUETE = "extrait tout le texte du livre que je te join ici"

def generer_avec_fichier(chemin_fichier: str) -> str:
    response = client.models.generate_content(
                                            model="gemini-1.5-flash",
                                            contents=[
                                                TEXTE_REQUETE,
                                                {"file-data": {"file_path": chemin_fichier}}
                                            ],
                                        )
    return response.text

for file in sorted(Path("parts").iterdir(), key=lambda f: int(f.stem.split("_")[1])):
    if file.is_file():
        print(f"Conversion du fichier : {file.name}")
        texte = generer_avec_fichier(str(file))
        print("--- Texte Extrait ---")
        print(texte[:500])
        print("...\n")

print(reponse.text)

filepath = pathlib.Path('~tmp/sortie_read_book')