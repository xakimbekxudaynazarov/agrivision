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
    try:
        file = camera_file or gallery_file
        if not file:
            return "<h3>❌ Rasm tanlanmadi</h3><a href='/'>⬅ Orqaga</a>"

        data = await file.read()

        if len(data) > 5 * 1024 * 1024:
            return "<h3>❌ Rasm juda katta (5MB dan kichik)</h3><a href='/'>⬅ Orqaga</a>"

        # 🔑 PIL orqali o‘qiymiz (format muammosiz)
        pil_img = Image.open(io.BytesIO(data)).convert("RGB")

        # OpenCV formatiga o‘tkazamiz
        img = np.array(pil_img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Safe resize
        h, w, _ = img.shape
        if max(h, w) > 400:
            scale = 400 / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        total = gray.size

        dark_ratio = np.sum(gray < 80) / total
        yellow_mask = cv2.inRange(hsv, (20, 80, 80), (35, 255, 255))
        yellow_ratio = np.sum(yellow_mask > 0) / total
        white_ratio = np.sum(gray > 220) / total
        std_dev = np.std(gray)

        findings = []

        if dark_ratio > 0.18:
            findings.append("⚫ Qora dog‘lar (zamburug‘)")
        if yellow_ratio > 0.25:
            findings.append("🟡 Sariqlik (oziqa yetishmasligi)")
        if white_ratio > 0.12:
            findings.append("⚪ Oqartgan joylar")
        if std_dev > 55:
            findings.append("🌈 Rang notekisligi")

        if not findings:
            result = "🌿 Barg sog‘lom"
            advice = "Parvarishni davom ettiring"
        else:
            result = "⚠️ Kasallik belgilari topildi"
            advice = "<br>".join(findings)

        return f"""
        <div style="font-family:Arial; text-align:center;">
            <h2>{result}</h2>
            <p>{advice}</p>
            <a href="/">⬅ Yana rasm yuklash</a>
        </div>
        """

    except Exception as e:
        return f"""
        <h3>❌ Server xatosi</h3>
        <pre>{str(e)}</pre>
        <a href="/">⬅ Orqaga</a>
        """
