import os
import base64
from mistralai import Mistral
from pdf2image import convert_from_path
from io import BytesIO

api_key= os.getenv("MISTRAL_API_KEY")
agent_id = "ag:376f91a9:20250922:pixstral:13a20876"

pages = convert_from_path("/home/m1gl/elise.magnier.etu/PJE_D/Dream_Team/biblioteko/exemples/copyrighted/cleaned_scan/QueSaisJe_1_LesÉtapesDeLaBiologie_1954_7_MauriceCaullery.pdf", dpi=200)

images_b64 = []
for i, page in enumerate(pages):
    buffer = BytesIO()
    page.save(buffer,  "PNG")
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    images_b64.append(b64)



messages = [{"role": "user", 
                "content": [
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{images_b64[0]}"},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{images_b64[1]}"}
                ]
            }
        ]
with Mistral(api_key=api_key) as client:
    resp = client.agents.complete(
        messages=messages,
        agent_id = agent_id,
        stream= False
    )
    print(resp.choices[0].message.content)