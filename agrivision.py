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
    </head>
    <body style="font-family:Arial;text-align:center">
        <h1>🌱 AgriVision ishlayapti</h1>
        <p>Internet orqali ochildi</p>

        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required>
            <br><br>
            <button type="submit">📷 Rasm yuklash</button>
        </form>
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
    return f"<h3>✅ Rasm qabul qilindi: {w} x {h}</h3><a href='/'>⬅ Yana yuklash</a>"
