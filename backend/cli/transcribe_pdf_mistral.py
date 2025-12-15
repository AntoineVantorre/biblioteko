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
import os
import base64
import re
import json
from pathlib import Path
from mistralai import Mistral

def parse_data_uri_image(data_uri):
    """
    Parse une data URI d'image et extrait le format et les données base64.
    
    Args:
        data_uri (str): Data URI au format "data:image/format;base64,base64_data"
        
    Returns:
        tuple: (format, base64_data) où format est l'extension et base64_data les données brutes
    """
    try:
        if not data_uri.startswith('data:'):
            # Si ce n'est pas une data URI, traiter comme des données base64 brutes
            return detect_image_format_from_data(data_uri), data_uri
            
        # Parser la data URI: data:image/jpeg;base64,/9j/4AAQ...
        header, b64_data = data_uri.split(',', 1)
        
        # Extraire le type MIME: data:image/jpeg;base64 -> image/jpeg
        mime_type = header.split(';')[0].replace('data:', '')
        
        # Convertir le type MIME en extension
        format_map = {
            'image/jpeg': 'jpg',
            'image/jpg': 'jpg', 
            'image/png': 'png',
            'image/gif': 'gif',
            'image/webp': 'webp',
            'image/bmp': 'bmp',
            'image/x-icon': 'ico',
            'image/vnd.microsoft.icon': 'ico'
        }
        
        img_format = format_map.get(mime_type, 'jpg')
        print(f"DEBUG: Parsed data URI - MIME: {mime_type}, Format: {img_format}")
        
        return img_format, b64_data
        
    except Exception as e:
        print(f"Warning: Could not parse data URI: {e}")
        # Fallback: essayer de détecter à partir des données
        return detect_image_format_from_data(data_uri), data_uri

def detect_image_format_from_data(base64_data):
    """
    Détecter le format d'image à partir des données base64 brutes.
    
    Args:
        base64_data (str): Données de l'image en base64
        
    Returns:
        str: Extension du fichier (png, jpg, jpeg, gif, webp, etc.)
    """
    try:
        # Si c'est une data URI, extraire seulement la partie base64
        if base64_data.startswith('data:'):
            base64_data = base64_data.split(',', 1)[1]
            
        # Décoder les premiers bytes pour identifier le type de fichier
        header = base64.b64decode(base64_data[:100])  # Prendre plus de bytes pour être sûr
        
        # Signatures de fichiers (magic numbers)
        if header.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'png'
        elif header.startswith(b'\xff\xd8\xff'):
            return 'jpg'
        elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
            return 'gif'
        elif header.startswith(b'RIFF') and b'WEBP' in header:
            return 'webp'
        elif header.startswith(b'BM'):
            return 'bmp'
        elif header.startswith(b'\x00\x00\x01\x00') or header.startswith(b'\x00\x00\x02\x00'):
            return 'ico'
        else:
            # Par défaut, supposer que c'est du JPEG (format le plus courant pour l'OCR)
            return 'jpg'
    except Exception as e:
        print(f"Warning: Could not detect image format from data: {e}")
        return 'jpg'  # Format par défaut

def fix_image_references(markdown_text, image_mapping):
    """
    Corriger les références d'images dans le texte Markdown pour qu'elles correspondent 
    aux fichiers réellement sauvegardés.
    
    Args:
        markdown_text (str): Texte Markdown avec les références d'images OCR
        image_mapping (dict): Mapping des noms OCR vers les vrais noms de fichiers
        
    Returns:
        str: Texte Markdown avec les références d'images corrigées
    """
    print(f"DEBUG: Fixing image references using mapping with {len(image_mapping)} entries")
    
    corrected_text = markdown_text
    corrections_made = 0
    
    # Pattern pour trouver les références d'images Markdown: ![alt](image.ext)
    import re
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    def replace_image_ref(match):
        nonlocal corrections_made
        alt_text = match.group(1)
        image_name = match.group(2)
        
        # Vérifier si cette image est dans notre mapping
        if image_name in image_mapping:
            new_image_name = image_mapping[image_name]
            corrections_made += 1
            print(f"DEBUG: Correcting image reference: {image_name} -> {new_image_name}")
            return f"![{alt_text}]({new_image_name})"
        else:
            # Essayer de trouver une correspondance approximative
            for ocr_name, real_name in image_mapping.items():
                if image_name.lower() in ocr_name.lower() or ocr_name.lower() in image_name.lower():
                    corrections_made += 1
                    print(f"DEBUG: Approximate correction: {image_name} -> {real_name}")
                    return f"![{alt_text}]({real_name})"
            
            print(f"DEBUG: No mapping found for image: {image_name}")
            return match.group(0)  # Retourner le texte original si pas de correspondance
    
    corrected_text = re.sub(pattern, replace_image_ref, corrected_text)
    
    print(f"DEBUG: Made {corrections_made} image reference corrections")
    return corrected_text

def transcribe_pdf(pdf_path, output_dir):
    """
    Transcrit un PDF en utilisant l'API Mistral OCR avec le SDK officiel.
    
    Args:
        pdf_path (str): Chemin vers le fichier PDF à transcrire
        output_dir (str): Dossier de sortie pour la transcription et les images
        
    Yields:
        str: Le contenu transcrit du PDF
    """
    api_key = os.environ.get("MISTRAL_API_KEY")
    agent_id = os.environ.get("MISTRAL_AGENT_ID")

    print(f"[mistral_ocr] transcribe_pdf called with pdf_path={pdf_path} output_dir={output_dir}")
    if api_key:
        print(f"[mistral_ocr] MISTRAL_API_KEY present: yes (masked)")
    else:
        print(f"[mistral_ocr] MISTRAL_API_KEY present: NO")
    if agent_id:
        print(f"[mistral_ocr] MISTRAL_AGENT_ID present: yes")
    else:
        print(f"[mistral_ocr] MISTRAL_AGENT_ID present: NO")

    if not api_key:
        raise ValueError("The environment variable MISTRAL_API_KEY is not set.")

    print(f"[mistral_ocr] Converting PDF '{pdf_path}' to OCR...")

    # Initialiser le client Mistral
    client = Mistral(api_key=api_key)
    
    try:
        # Méthode 1: Utiliser base64 (recommandée dans la doc pour les fichiers locaux)
        def encode_pdf(pdf_path):
            """Encode le PDF en base64."""
            try:
                with open(pdf_path, "rb") as pdf_file:
                    return base64.b64encode(pdf_file.read()).decode('utf-8')
            except FileNotFoundError:
                print(f"Error: Le fichier {pdf_path} n'a pas été trouvé.")
                return None
            except Exception as e:
                print(f"Error: {e}")
                return None
        
        print(f"[mistral_ocr] Encoding PDF '{pdf_path}' to base64...")
        base64_pdf = encode_pdf(pdf_path)
        if not base64_pdf:
            print("[mistral_ocr] encode_pdf returned None")
            raise Exception("Impossible d'encoder le PDF en base64")
        print(f"[mistral_ocr] Encoded PDF -> base64 length: {len(base64_pdf)} chars (~{len(base64_pdf)/1024/1024:.2f} MB)")
        
        print("[mistral_ocr] Processing PDF with OCR (using official SDK)...")

        # Étape 2: Traitement OCR avec le SDK officiel
        try:
            ocr_response = client.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "document_url",
                    "document_url": f"data:application/pdf;base64,{base64_pdf}"
                },
                include_image_base64=True  # CLEF: Cette option permet d'avoir les images !
            )
        except Exception as e:
            print(f"[mistral_ocr] client.ocr.process raised exception: {e}")
            raise
        
        # Convertir la réponse en dictionnaire pour compatibilité
        ocr_result = ocr_response.model_dump() if hasattr(ocr_response, 'model_dump') else ocr_response.dict()
        
        num_pages = ocr_result.get('usage_info', {}).get('pages_processed', 0)
        print(f"[mistral_ocr] OCR returned result keys: {list(ocr_result.keys())}")
        print(f"[mistral_ocr] The PDF contains {num_pages} pages (reported)")
        
        # Extraction du texte et des images de la réponse OCR
        extracted_text = ""
        images_data = []
        
        # Le dossier de sortie est maintenant le dossier de l'œuvre
        work_dir = Path(output_dir)
        work_dir.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarde complète de la réponse OCR pour debug
        import json
        debug_file = work_dir / "ocr_response_debug.json"

        with open(debug_file, "w", encoding="utf-8") as f:
            json.dump(ocr_result, f, indent=2, ensure_ascii=False)
        print(f"[mistral_ocr] Full OCR response saved to {debug_file} (size={debug_file.stat().st_size} bytes)")
        
        if 'pages' in ocr_result:
            print(f"DEBUG: Found {len(ocr_result['pages'])} pages in OCR result")
            
            for page_idx, page in enumerate(ocr_result['pages']):
                print(f"\nDEBUG: Processing page {page_idx}")
                print(f"DEBUG: Page keys: {list(page.keys())}")
                
                if 'markdown' in page:
                    extracted_text += page['markdown'] + "\n\n"
                
                # Extraction des images si présentes
                if 'images' in page:
                    print(f"DEBUG: Found {len(page['images'])} images on page {page_idx}")
                    
                    for img_idx, image_data in enumerate(page['images']):
                        print(f"\nDEBUG: Processing image {img_idx} on page {page_idx}")
                        print(f"DEBUG: Image data keys: {list(image_data.keys())}")
                        
                        # Afficher toute la structure de l'image (mais limiter image_base64 si présent)
                        debug_image_data = {}
                        for key, value in image_data.items():
                            if key == 'image_base64' and value is not None:
                                debug_image_data[key] = f"<base64 data, length: {len(value)}>"
                            else:
                                debug_image_data[key] = value
                        print(f"DEBUG: Image data structure: {debug_image_data}")
                        
                        if 'image_base64' in image_data:
                            if image_data['image_base64'] is not None:
                                # Parser la data URI de l'image pour extraire le format et les données
                                img_data_uri = image_data['image_base64']
                                img_format, img_base64_data = parse_data_uri_image(img_data_uri)
                                img_filename = f"img-{page_idx}-{img_idx}.{img_format}"
                                
                                images_data.append({
                                    'filename': img_filename,
                                    'data': img_base64_data,  # Données base64 pures (sans le préfixe data URI)
                                    'page': page_idx
                                })
                                print(f"SUCCESS: Image {img_idx} on page {page_idx} added to queue (format: {img_format})")
                            else:
                                print(f"WARNING: image_base64 is None for image {img_idx} on page {page_idx}")
                        else:
                            print(f"WARNING: No 'image_base64' key found for image {img_idx} on page {page_idx}")
                else:
                    print(f"DEBUG: No images found on page {page_idx}")
        else:
            print("DEBUG: No 'pages' key found in OCR result")
            print(f"DEBUG: OCR result keys: {list(ocr_result.keys())}")
        
        if not extracted_text.strip():
            print("[mistral_ocr] WARNING: extracted_text is empty after OCR processing")
            # Save a quick debug snippet
            snippet_file = work_dir / "ocr_extracted_text_snippet.txt"
            snippet_file.write_text(json.dumps(ocr_result.get('pages', [])[:3], ensure_ascii=False), encoding='utf-8')
            print(f"[mistral_ocr] Wrote snippet to {snippet_file}")
            raise Exception("No text extracted from OCR")
            
        # Sauvegarde des images dans le dossier de l'œuvre et création de la table de correspondance
        print(f"\nDEBUG: Attempting to save {len(images_data)} images to {work_dir}")
        image_mapping = {}  # Mapping des noms d'images OCR vers les vrais noms de fichiers
        
        for img_info in images_data:
            img_path = work_dir / img_info['filename']
            print(f"DEBUG: Saving image to {img_path}")
            try:
                # Décoder l'image base64 et la sauvegarder
                img_data = base64.b64decode(img_info['data'])
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"SUCCESS: Image saved: {img_info['filename']} ({len(img_data)} bytes)")
                
                # Créer le mapping pour corriger les références dans le markdown
                # Format OCR typique: img-0.jpeg, img-1.jpeg, etc.
                # Format sauvegardé: img-{page}-{index}.{extension}
                page_idx = img_info['page']
                # Trouver l'index de l'image sur cette page
                page_images = [img for img in images_data if img['page'] == page_idx]
                img_index_on_page = page_images.index(img_info)
                
                # Calculer l'index global approximatif (pour correspondre aux références OCR)
                global_img_index = sum(1 for img in images_data[:images_data.index(img_info)])
                
                # Mapping des différents formats possibles
                ocr_patterns = [
                    f"img-{global_img_index}.jpeg",
                    f"img-{global_img_index}.jpg", 
                    f"img-{global_img_index}.png",
                    f"img-{page_idx}.jpeg",
                    f"img-{page_idx}.jpg",
                    f"img-{page_idx}.png"
                ]
                
                for pattern in ocr_patterns:
                    image_mapping[pattern] = img_info['filename']
                    
            except Exception as e:
                print(f"ERROR: Could not save image {img_info['filename']}: {e}")
                import traceback
                traceback.print_exc()
            
        # Étape 3: Correction des références d'images dans le texte
        print(f"[mistral_ocr] Correcting image references in extracted text... (mapping size={len(image_mapping)})")
        extracted_text = fix_image_references(extracted_text, image_mapping)
        
        # Étape 4: Amélioration avec l'agent Mistral (optionnel)
        if agent_id:
            try:
                print("Enhancing transcription with Mistral agent...")
                
                # Utiliser le SDK pour l'agent également
                agent_response = client.agents.complete(
                    agent_id=agent_id,
                    messages=[
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
                )
                raise Exception("Impossible d'encoder le PDF en base64")
                
                # Extraire le contenu de la réponse
                if hasattr(agent_response, 'choices') and agent_response.choices:
                    enhanced_text = agent_response.choices[0].message.content
                    if enhanced_text:
                        # Corriger aussi les références d'images dans le texte amélioré
                        enhanced_text = fix_image_references(enhanced_text, image_mapping)
                        yield enhanced_text
                    else:
                        print("\nNo enhanced content received, using raw OCR text.")
                        yield extracted_text
                else:
                    print("\nNo enhanced content received, using raw OCR text.")
                    yield extracted_text
                    
            except Exception as e:
                print(f"\nAgent enhancement error: {e}")
                print("Using raw OCR text instead")
                yield extracted_text
        else:
            yield extracted_text
            
        print("[mistral_ocr] OCR processing completed successfully.")
            
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
    work_dir = Path(output_dir) / pdf_name
    markdown_file = work_dir / f"{pdf_name}.md"

    try:
        print("\n" + "=" * 50)
        print("TRANSCRIPTION:")
        print("=" * 50)
        print(f"Output directory: {output_dir}")
        print(f"Work directory: {work_dir}")
        print(f"Markdown file: {markdown_file}")
        
        # Créer le dossier de sortie s'il n'existe pas
        work_dir.mkdir(parents=True, exist_ok=True)
        
        with open(markdown_file, "w", encoding="utf-8") as f:
            total_written = 0
            for transcription in transcribe_pdf(pdf_path, str(work_dir)):
                f.write(transcription)
                f.flush()
                total_written += len(transcription)
        print(f"\nResult written to {markdown_file} (bytes_written={total_written})")
        print("\n" + "=" * 50)
        print("Transcription complete.")
        print("=" * 50)
    except Exception as e:
        print(f"Error: {e}")
        print("=" * 50)