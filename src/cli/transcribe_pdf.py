import os
import base64
import argparse
from tqdm import tqdm
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
    agent_id = os.getenv("MISTRAL_AGENT_ID")

    if not api_key:
        raise ValueError("The environment variable MISTRAL_API_KEY is not set.")

    print(f"Converting PDF '{pdf_path}' to images...")
    pages = convert_from_path(pdf_path, dpi=200)
    num_pages = len(pages)
    print(f"The PDF contains {num_pages} pages.")

    try:
        with Mistral(api_key=api_key) as client:
            last_transcriptions = []  # Contexte des deux dernières réponses du lot précédent
            batch_size = 5
            with tqdm(total=num_pages, desc="Transcription", unit="page") as pbar:
                for batch_start in range(0, num_pages, batch_size):
                    batch_pages = pages[batch_start:batch_start+batch_size]
                    batch_contents = []
                    for page in batch_pages:
                        buffer = BytesIO()
                        page.save(buffer, "JPEG")
                        buffer.seek(0)
                        b64 = base64.b64encode(buffer.read()).decode()
                        batch_contents.append({"type": "image_url", "image_url": f"data:image/jpeg;base64,{b64}"})

                    messages = []
                    # Ajoute les deux dernières transcriptions comme contexte (rôle assistant)
                    for previous in last_transcriptions:
                        messages.append({"role": "assistant", "content": previous})
                    # Ajoute une instruction si ce n'est pas le premier lot
                    if batch_start > 0:
                        instruction = "Note: The following pages are not the beginning of the document. If you encounter a chapter title, format it as a level 2 heading (##) in Markdown, not level 1 (#)."
                        messages.append({"role": "user", "content": instruction})
                    # Ajoute le lot de pages (rôle user)
                    messages.append({"role": "user", "content": batch_contents})

                    try:
                        resp = client.agents.complete(
                            messages=messages,
                            agent_id=agent_id,
                            stream=False
                        )
                        transcribed_content = resp.choices[0].message.content if resp.choices[0].message else ""
                        if not transcribed_content:
                            print("\nNo content received for this batch or the response is empty.")
                        yield transcribed_content
                        # Met à jour le contexte (garde les deux dernières lots)
                        last_transcriptions.append(transcribed_content)
                        if len(last_transcriptions) > 3:
                            last_transcriptions.pop(0)
                    except Exception as e:
                        print(f"Error while transcribing batch of pages {batch_start+1}-{min(batch_start+batch_size, num_pages)}: {str(e)}")
                    pbar.update(len(batch_pages))
        print("="*50)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe a PDF to markdown from images, using the Mistral API.")
    parser.add_argument('-i', '--input', required=True, help='Path to the PDF file to transcribe')
    parser.add_argument('-o', '--output', required=True, help='Path to the output markdown file')
    args = parser.parse_args()

    pdf_path = args.input
    output_file = args.output

    try:
        print("\n" + "="*50)
        print("TRANSCRIPTION:")
        print("="*50)
        with open(output_file, "w", encoding="utf-8") as f:
            for transcription in transcribe_pdf(pdf_path):
                f.write(transcription)
                f.flush()
        print(f"\nResult written to {output_file}")
        print("\n" + "="*50)
        print("Transcription complete.")
        print("="*50)
    except Exception as e:
        print(f"Error: {e}")
        print("="*50)
    except Exception as e:
        print(f"Erreur: {e}")