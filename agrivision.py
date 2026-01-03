from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from typing import Optional
import cv2
import numpy as np
import base64


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AgriVision</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial; background:#f4f6f7; text-align:center; }
            .box {
                background:white; padding:20px; margin:40px auto;
                max-width:400px; border-radius:10px;
            }
            label { display:block; margin:10px; font-size:16px; cursor:pointer; }
            button { padding:10px 20px; font-size:16px; margin-top:15px; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>🌱 AgriVision</h2>

            <form action="/upload" method="post" enctype="multipart/form-data">

                <label>
                    📸 Kameradan olish
                    <input type="file" name="camera_file"
                           accept="image/*" capture="environment" hidden>
                </label>

                <label>
                    🖼️ Galareyadan tanlash
                    <input type="file" name="gallery_file"
                           accept=".jpg,.jpeg,.png" hidden>
                </label>

                <button type="submit">📤 Yuborish</button>
            </form>
        </div>
    </body>
    </html>
    """


from PIL import Image
import io

@app.post("/upload", response_class=HTMLResponse)
async def upload(
    camera_file: Optional[UploadFile] = File(None),
    gallery_file: Optional[UploadFile] = File(None)
):
    file = camera_file or gallery_file
    if not file:
        return "<h3>❌ Rasm tanlanmadi</h3><a href='/'>⬅ Orqaga</a>"

    data = await file.read()

    if not data:
        return "<h3>❌ Fayl bo‘sh</h3><a href='/'>⬅ Orqaga</a>"

    # 📷 RASMNI BASE64 GA O‘TKAZAMIZ
    img_base64 = base64.b64encode(data).decode("utf-8")

    # OpenCV orqali o‘qiymiz (kamera JPEG)
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return "<h3>❌ Rasm o‘qilmadi</h3><a href='/'>⬅ Orqaga</a>"

    # Kichraytiramiz
    img = cv2.resize(img, (300, 300))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    total = gray.size
    dark_ratio = np.sum(gray < 80) / total

    # 📊 FOIZ HISOBI
    disease_percent = min(int(dark_ratio * 300), 100)
    healthy_percent = 100 - disease_percent

    if disease_percent > 30:
        result = "⚠️ Kasallik ehtimoli yuqori"
    else:
        result = "🌿 Barg sog‘lom ko‘rinadi"

    return f"""
    <div style="font-family:Arial; text-align:center;">
        <h2>{result}</h2>

        <img src="data:image/jpeg;base64,{img_base64}"
             style="max-width:300px;border-radius:10px;margin:15px 0;"/>

        <p>⚠️ Kasallik ehtimoli: <b>{disease_percent}%</b></p>
        <p>🌿 Sog‘lom ehtimoli: <b>{healthy_percent}%</b></p>

        <a href="/">⬅ Yana rasm yuklash</a>
    </div>
    """

