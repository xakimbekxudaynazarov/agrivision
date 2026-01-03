from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
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
            body { font-family: Arial; text-align: center; background:#f4f6f7; }
            .box { background:white; padding:20px; margin:40px auto; max-width:400px; border-radius:10px; }
            button { padding:10px 20px; font-size:16px; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>🌱 AgriVision</h2>
            <p>Rasm yuklang</p>

           <form action="/upload" method="post" enctype="multipart/form-data">

  <label style="display:block; margin:10px;">
    📸 Kameradan olish
    <input type="file" name="file" accept="image/*" capture="environment" hidden>
  </label>

  <label style="display:block; margin:10px;">
    🖼️ Galareyadan tanlash
    <input type="file" name="file" accept="image/*" hidden>
  </label>

  <button type="submit">Yuborish</button>
</form>

        </div>
    </body>
    </html>
    """

@app.post("/upload", response_class=HTMLResponse)
async def upload(file: UploadFile = File(...)):
    data = await file.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        return "<h3>❌ Rasm o‘qilmadi</h3><a href='/'>⬅ Orqaga</a>"

    h, w, _ = img.shape
    return f"""
    <h2>✅ Rasm qabul qilindi</h2>
    <p>O‘lchami: {w} x {h}</p>
    <a href="/">⬅ Yana rasm yuklash</a>
    """



