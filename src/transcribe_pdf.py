import os
import base64
from mistralai import Mistral
from pdf2image import convert_from_path
from io import BytesIO

def transcribe_pdf(pdf_path):
    """
    Transcrit un PDF en utilisant l'API Mistral.
    
    Args:
        pdf_path (str): Chemin vers le fichier PDF à transcrire
        
    Returns:
        str: Le contenu transcrit de toutes les pages du PDF
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    agent_id = "ag:376f91a9:20250922:pixstral:13a20876"
    
    if not api_key:
        raise ValueError("MISTRAL_API_KEY n'est pas définie dans les variables d'environnement")
    
    print(f"Conversion du PDF '{pdf_path}' en images...")
    pages = convert_from_path(pdf_path, dpi=200)
    print(f"Le PDF contient {len(pages)} pages.")

    try:
        with Mistral(api_key=api_key) as client:
            for i, page in enumerate(pages):
                buffer = BytesIO()
                page.save(buffer, "JPEG")
                buffer.seek(0)
                b64 = base64.b64encode(buffer.read()).decode()
                content = [{"type": "image_url", "image_url": f"data:image/jpeg;base64,{b64}"}]
                messages = [{"role": "user", "content": content}]
                try:
                    resp = client.agents.complete(
                        messages=messages,
                        agent_id=agent_id,
                        stream=False
                    )
                    transcribed_content = resp.choices[0].message.content if resp.choices[0].message else ""
                    if not transcribed_content:
                        print("\nAucun contenu reçu pour cette page ou la réponse est vide.")
                    print(transcribed_content)
                    yield transcribed_content
                except Exception as e:
                    print(f"Erreur lors de la transcription de la page {i+1}: {str(e)}")
        print("="*50)
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    pdf_path = "./exemples/copyrighted/cleaned_scan/QueSaisJe_1_LesÉtapesDeLaBiologie_1954_7_MauriceCaullery.pdf"
    try:
        print("\n" + "="*50)
        print("RÉSULTAT DE LA TRANSCRIPTION:")
        print("="*50)
        output_file = "QueSaisJe_1_LesÉtapesDeLaBiologie_1954_7_MauriceCaullery.md"
        with open(output_file, "w", encoding="utf-8") as f:
            for transcription in transcribe_pdf(pdf_path):
                f.write(transcription)
                f.flush()
        print(f"\nRésultat écrit dans {output_file}")
        print("\n" + "="*50)
        print("Transcription complète.")
        print("="*50)
    except Exception as e:
        print(f"Erreur: {e}")