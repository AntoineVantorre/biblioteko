#!/usr/bin/env python3

"""
Transcription de PDFs scannés avec l'API Mistral OCR

Ce script utilise l'API Mistral pour:
1. Uploader un PDF vers Mistral Files API
2. Traiter le PDF avec l'OCR Mistral (mistral-ocr-latest)
3. Optionnellement améliorer le texte avec un agent Mistral
4. Sauvegarder le résultat en Markdown

Utilisation:
    python transcribe_pdf_mistral.py -i input.pdf -o output.md

Variables d'environnement requises:
    MISTRAL_API_KEY: Clé API Mistral
    MISTRAL_AGENT_ID: ID de l'agent (optionnel pour amélioration)
"""

import argparse
import requests
import os
import base64
import re
from pathlib import Path

def transcribe_pdf(pdf_path, output_dir):
    """
    Transcrit un PDF en utilisant l'API Mistral OCR.
    
    Args:
        pdf_path (str): Chemin vers le fichier PDF à transcrire
        output_dir (str): Dossier de sortie pour la transcription et les images
        
    Yields:
        str: Le contenu transcrit du PDF
    """
    api_key = os.environ.get("MISTRAL_API_KEY")
    agent_id = os.environ.get("MISTRAL_AGENT_ID")
    
    if not api_key:
        raise ValueError("The environment variable MISTRAL_API_KEY is not set.")
    
    print(f"Converting PDF '{pdf_path}' to OCR...")

    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        # Étape 1: Upload du fichier PDF
        print(f"Uploading PDF '{pdf_path}'...")
        
        with open(pdf_path, "rb") as f:
            files = {"file": (Path(pdf_path).name, f, "application/pdf")}
            data = {"purpose": "ocr"}
            
            upload_response = requests.post(
                "https://api.mistral.ai/v1/files",
                files=files,
                data=data,
                headers=headers,
                timeout=120
            )
        
        if upload_response.status_code != 200:
            raise Exception(f"Upload failed: {upload_response.status_code} - {upload_response.text}")
        
        file_info = upload_response.json()
        file_id = file_info["id"]
        print(f"PDF uploaded successfully. Processing with OCR...")
        
        # Étape 2: Traitement OCR
        ocr_payload = {
            "document": {
                "type": "file",
                "file_id": file_id
            },
            "model": "mistral-ocr-latest"
        }
        
        ocr_response = requests.post(
            "https://api.mistral.ai/v1/ocr",
            json=ocr_payload,
            headers=headers,
            timeout=300
        )
        
        if ocr_response.status_code != 200:
            raise Exception(f"OCR failed: {ocr_response.status_code} - {ocr_response.text}")
        
        ocr_result = ocr_response.json()
        num_pages = ocr_result.get('usage_info', {}).get('pages_processed', 0)
        print(f"The PDF contains {num_pages} pages.")
        
        # Extraction du texte et des images de la réponse OCR
        extracted_text = ""
        images_data = []
        
        if 'pages' in ocr_result:
            for page_idx, page in enumerate(ocr_result['pages']):
                if 'markdown' in page:
                    extracted_text += page['markdown'] + "\n\n"
                
                # Extraction des images si présentes
                if 'images' in page:
                    for img_idx, image_data in enumerate(page['images']):
                        if 'data' in image_data:
                            img_filename = f"img-{page_idx}-{img_idx}.jpeg"
                            images_data.append({
                                'filename': img_filename,
                                'data': image_data['data'],
                                'page': page_idx
                            })
        
        if not extracted_text.strip():
            raise Exception("No text extracted from OCR")
            
        # Création du dossier de sortie et sauvegarde des images
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarde des images
        for img_info in images_data:
            img_path = output_path / img_info['filename']
            try:
                # Décoder l'image base64 et la sauvegarder
                img_data = base64.b64decode(img_info['data'])
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Image saved: {img_info['filename']}")
            except Exception as e:
                print(f"Warning: Could not save image {img_info['filename']}: {e}")
            
        # Étape 3: Amélioration avec l'agent Mistral (optionnel)
        if agent_id:
            try:
                enhancement_payload = {
                    "agent_id": agent_id,
                    "messages": [
                        {
                            "role": "user", 
                            "content": f"""You are an expert in transcribing books. Here is the raw OCR text from a scanned book that you must improve and correct to produce a high-quality Markdown transcription.

CRITICAL: YOU MUST TRANSCRIBE THE ENTIRE BOOK - DO NOT STOP AFTER A FEW PAGES. Process ALL the content provided, from the beginning to the very end of the book.

PRECISE INSTRUCTIONS:

1. **Output Format**: Markdown only, scrupulously respecting the original book structure

2. **OCR Error Correction**:
   - Fix character recognition errors (misrecognized letters, truncated words)
   - Reconstruct words and sentences broken at line and page endings
   - Correct misrecognized punctuation
   - Repair special characters and accents

3. **Structure and Formatting**:
   - Faithfully respect the hierarchy of titles from the original book
   - Use consistent Markdown header hierarchy (# ## ### etc.)
   - Preserve paragraph structure, lists, and quotations
   - Maintain natural page breaks from the book

4. **CRITICAL: Paragraph Reconstruction Across Pages**:
   - **Merge text fragments** that are split across page boundaries to form coherent paragraphs
   - **Reconstruct complete sentences** when they are broken between pages
   - **Join continuation text** from one page to the next when it's part of the same paragraph
   - **Identify logical paragraph breaks** vs. artificial page breaks
   - **Ensure textual continuity** - if a sentence or paragraph continues on the next page, merge it seamlessly
   - **Remove artificial line breaks** caused by page boundaries within paragraphs
   - The goal is to have **flowing, complete paragraphs** as they would appear in a continuous text

5. **Elements to EXCLUDE**:
   - Do not include repetitive page headers
   - Do not include repetitive footers (page numbers, publisher names)
   - Remove scanning artifacts

6. **Footnotes and References**:
   - Integrate footnotes at their logical placement in the text
   - Use appropriate Markdown syntax for references
   - Preserve all important bibliographic information

7. **Images and Diagrams**:
   - Indicate the location of images/diagrams with descriptive markers
   - Format: `![Description of image/diagram](image_location)`
   - Briefly describe visual content if relevant for understanding

8. **Content Fidelity**:
   - DO NOT alter, summarize, or paraphrase the original content
   - Preserve the writing style and vocabulary of the era
   - Maintain scientific and literary integrity of the text
   - Keep citations, references, and exact data

9. **Typographic Consistency and Visual Organization**:
   - **Standardize title formats** throughout the entire book - use identical header levels for similar content types
   - **Maintain consistent formatting** across all sections and chapters
   - **Preserve visual hierarchy** - ensure similar elements are formatted identically throughout the work
   - **Tables of Contents**: Keep visually organized with proper indentation and consistent formatting
   - **Lists and enumerations**: Use consistent bullet points, numbering, and indentation patterns
   - **Chapter/section breaks**: Apply uniform spacing and formatting between major sections
   - **Bibliography and references**: Maintain consistent citation formatting throughout
   - **Special text elements** (quotes, examples, definitions): Use consistent Markdown formatting
   - Respect French typographic conventions
   - Maintain professional and readable presentation across the entire document

Here is the raw OCR text to process:

{extracted_text}

**IMPORTANT: This appears to be a {num_pages}-page document. You MUST transcribe the ENTIRE content provided above, from the very first page to the very last page. Do not stop after the preliminary pages or table of contents. Process ALL chapters, sections, and content through to the conclusion and any appendices.**

Produce a perfectly formatted Markdown transcription, faithful to the original book, without repetitive headers/footers, with consistent structure and all necessary OCR corrections."""
                        }
                    ]
                }
                
                enhancement_response = requests.post(
                    "https://api.mistral.ai/v1/agents/completions",
                    json=enhancement_payload,
                    headers=headers,
                    timeout=600
                )
                
                if enhancement_response.status_code == 200:
                    enhancement_result = enhancement_response.json()
                    if 'choices' in enhancement_result and enhancement_result['choices']:
                        enhanced_text = enhancement_result['choices'][0]['message']['content']
                        if enhanced_text:
                            yield enhanced_text
                        else:
                            print("\nNo enhanced content received, using raw OCR text.")
                            yield extracted_text
                    else:
                        print("\nNo enhanced content received, using raw OCR text.")
                        yield extracted_text
                else:
                    print(f"\nAgent enhancement failed: {enhancement_response.status_code}")
                    print("Using raw OCR text instead")
                    yield extracted_text
            except Exception as e:
                print(f"\nAgent enhancement error: {e}")
                print("Using raw OCR text instead")
                yield extracted_text
        else:
            yield extracted_text
        
        # Étape 4: Nettoyage
        try:
            delete_response = requests.delete(
                f"https://api.mistral.ai/v1/files/{file_id}",
                headers=headers
            )
            if delete_response.status_code != 200:
                print(f"Warning: Could not delete file {file_id}: {delete_response.status_code}")
        except Exception as e:
            print(f"Warning: Error deleting file: {e}")
            
        print("=" * 50)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe a PDF to markdown using the Mistral OCR API.")
    parser.add_argument('-i', '--input', required=True, help='Path to the PDF file to transcribe')
    parser.add_argument('-o', '--output', required=True, help='Path to the output directory (will contain markdown file and images)')
    args = parser.parse_args()

    pdf_path = args.input
    output_dir = args.output

    # Créer le nom du fichier markdown basé sur le nom du PDF
    pdf_name = Path(pdf_path).stem
    markdown_file = Path(output_dir) / f"{pdf_name}.md"

    try:
        print("\n" + "=" * 50)
        print("TRANSCRIPTION:")
        print("=" * 50)
        print(f"Output directory: {output_dir}")
        print(f"Markdown file: {markdown_file}")
        
        with open(markdown_file, "w", encoding="utf-8") as f:
            for transcription in transcribe_pdf(pdf_path, output_dir):
                f.write(transcription)
                f.flush()
        print(f"\nResult written to {markdown_file}")
        print("\n" + "=" * 50)
        print("Transcription complete.")
        print("=" * 50)
    except Exception as e:
        print(f"Error: {e}")
        print("=" * 50)