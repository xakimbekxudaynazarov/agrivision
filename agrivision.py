from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from typing import Optional
import cv2
import numpy as np

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
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f7;
                text-align: center;
            }
            .box {
                background: white;
                padding: 20px;
                margin: 40px auto;
                max-width: 400px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                margin-top: 15px;
                cursor: pointer;
            }
            label {
                display: block;
                margin: 10px;
                font-size: 16px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>🌱 AgriVision ishlayapti</h2>
            <p>Internet orqali ochildi</p>

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


@app.post("/upload", response_class=HTMLResponse)
async def upload(
    camera_file: Optional[UploadFile] = File(None),
    gallery_file: Optional[UploadFile] = File(None)
):
    file = camera_file or gallery_file

    if not file:
        return """
        <h3>❌ Rasm tanlanmadi</h3>
        <a href="/">⬅ Orqaga</a>
        """

    data = await file.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        return """
        <h3>❌ Rasm o‘qilmadi</h3>
        <a href="/">⬅ Orqaga</a>
        """

    h, w, _ = img.shape

    return f"""
    <div style="text-align:center; font-family:Arial;">
        <h2>✅ Rasm qabul qilindi</h2>
        <p>O‘lchami: {w} x {h}</p>
        <a href="/">⬅ Yana rasm yuklash</a>
    </div>
    """
