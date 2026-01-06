from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import subprocess
import uuid
import os
import time
from dotenv import load_dotenv

router = APIRouter()


@router.post("/transcribe")
async def transcribe_upload(file: UploadFile = File(...), prefix: str = None):
    """Accept an uploaded PDF, run formatting then OCR transcription, and return markdown."""
    # Create working dir
    work_root = Path("/tmp/biblioteko_transcriptions")
    work_root.mkdir(parents=True, exist_ok=True)
    job_id = str(int(time.time())) + "-" + uuid.uuid4().hex[:6]
    work_dir = work_root / job_id
    work_dir.mkdir()

    try:
        print(f"[transcribe_api] Job {job_id} start, work_dir={work_dir}")
        # Save uploaded file
        filename = Path(file.filename).name
        saved_pdf = work_dir / filename
        with saved_pdf.open("wb") as f:
            shutil.copyfileobj(file.file, f)
        print(f"[transcribe_api] Saved uploaded PDF to {saved_pdf} (size={saved_pdf.stat().st_size} bytes)")

        pdf_stem = saved_pdf.stem

        # Step 1: run format_small_book.py with prefix set to the stem so output filename is predictable
        format_script = Path(__file__).resolve().parents[3] / "cli" / "format_small_book.py"
        transcribe_script = Path(__file__).resolve().parents[3] / "cli" / "transcribe_pdf_mistral.py"

        # Call format_small_book.py (may be optional), produce output into work_dir
        formatted_pdf = work_dir / f"{pdf_stem}.pdf"
        try:
            print(f"[transcribe_api] Invoking format script")
            proc = subprocess.run([
                "python3",
                str(format_script),
                "-i",
                str(saved_pdf),
                "-o",
                str(work_dir),
                "--prefix",
                pdf_stem
            ], capture_output=True, text=True)
            print(proc)
            if proc.returncode == 0:
                print(f"[transcribe_api] Format script completed (rc=0)")
            else:
                print(f"[transcribe_api] Format script exited with rc={proc.returncode} (continuing)")
        except Exception as e:
            print(f"[transcribe_api] Exception while running format script: {e}")
            pass
        input_for_ocr = formatted_pdf if formatted_pdf.exists() else saved_pdf
        # Ensure Mistral API key is available in environment (required by transcribe script)
        load_dotenv()  # Load .env if present
        if not os.environ.get("MISTRAL_API_KEY"):
            raise HTTPException(status_code=500, detail="MISTRAL_API_KEY not set in backend environment; OCR transcription cannot run.")

        # Call transcribe_pdf_mistral.py
        try:
            print(f"[transcribe_api] Running transcription script: {transcribe_script} on {input_for_ocr}")
            proc = subprocess.run([
                "python3",
                str(transcribe_script),
                "-i",
                str(input_for_ocr),
                "-o",
                str(work_dir)
            ], check=True, capture_output=True, text=True)
            print(f"[transcribe_api] Transcription script completed. stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"[transcribe_api] Transcription script failed. stdout:\n{e.stdout}\nstderr:\n{e.stderr}")
            raise HTTPException(status_code=500, detail=f"Transcription failed: {e.stderr or e.stdout}")

        # Read produced markdown file
        # The transcription script creates a subfolder named after the PDF stem
        md_file = work_dir / f"{pdf_stem}.md"
        if not md_file.exists():
            candidate = work_dir / pdf_stem / f"{pdf_stem}.md"
            if candidate.exists():
                md_file = candidate
            else:
                # Try to find any .md file recursively in work_dir
                mds = list(work_dir.rglob("*.md"))
                if not mds:
                    raise HTTPException(status_code=500, detail="No markdown output produced")
                md_file = mds[0]

        content = md_file.read_text(encoding="utf-8")
        print(f"[transcribe_api] Returning markdown from {md_file} (len={len(content)} chars)")

        # Inline images referenced in the markdown using data URIs so the frontend can render them
        def _guess_mime(ext: str) -> str:
            ext = ext.lower().lstrip('.')
            return {
                'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'gif': 'image/gif',
                'webp': 'image/webp', 'bmp': 'image/bmp', 'svg': 'image/svg+xml'
            }.get(ext, 'application/octet-stream')

        import re, base64

        def _inline_images(markdown_text: str, base_dir: Path) -> str:
            pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

            def _replace(m):
                alt = m.group(1)
                img_ref = m.group(2)

                # Only handle simple filenames or relative paths
                img_path = (base_dir / img_ref).resolve() if not Path(img_ref).is_absolute() else Path(img_ref)
                if not img_path.exists():
                    # try relative to markdown file directory
                    candidate = base_dir / img_ref
                    if candidate.exists():
                        img_path = candidate
                    else:
                        return m.group(0)

                try:
                    data = img_path.read_bytes()
                    ext = img_path.suffix.lstrip('.')
                    mime = _guess_mime(ext)
                    b64 = base64.b64encode(data).decode('ascii')
                    return f"![{alt}](data:{mime};base64,{b64})"
                except Exception as e:
                    print(f"[transcribe_api] Could not inline image {img_path}: {e}")
                    return m.group(0)

            return pattern.sub(_replace, markdown_text)

        content_inlined = _inline_images(content, md_file.parent)
        return {"markdown": content_inlined, "work_dir": str(work_dir)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))