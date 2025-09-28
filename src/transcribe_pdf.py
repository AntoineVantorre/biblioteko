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
    
    # Convertir toutes les pages du PDF en images
    pages = convert_from_path(pdf_path, dpi=200)
    
    # Encoder toutes les pages en base64
    images_b64 = []
    for i, page in enumerate(pages):
        buffer = BytesIO()
        page.save(buffer, "PNG")
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode()
        images_b64.append(b64)
    
    # Créer le contenu des messages en incluant toutes les pages
    content = []
    for b64_image in images_b64:
        content.append({"type": "image_url", "image_url": f"data:image/jpeg;base64,{b64_image}"})
    
    messages = [{"role": "user", "content": content}]
    
    # Envoyer la requête à l'API Mistral
    try:
        with Mistral(api_key=api_key) as client:
            print("Envoi de la requête à l'API Mistral...")
            resp = client.agents.complete(
                messages=messages,
                agent_id=agent_id,
                stream=False
            )
            
            # Retourner tout le contenu transcrit
            transcribed_content = resp.choices[0].message.content
            print(f"Transcription terminée. Contenu reçu: {len(transcribed_content)} caractères")
            return transcribed_content
            
    except Exception as e:
        raise Exception(f"Erreur lors de la transcription: {str(e)}")

# Exemple d'utilisation
if __name__ == "__main__":
    pdf_path = "./exemples/copyrighted/cleaned_scan/QueSaisJe_1_LesÉtapesDeLaBiologie_1954_7_MauriceCaullery.pdf"
    
    try:
        result = transcribe_pdf(pdf_path)
        print("\n" + "="*50)
        print("RÉSULTAT DE LA TRANSCRIPTION:")
        print("="*50)
        print(result)
        print("="*50)
    except Exception as e:
        print(f"Erreur: {e}")