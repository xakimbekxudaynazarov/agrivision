from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>AgriVision</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family:Arial; text-align:center">
        <h1>🌱 AgriVision ishlayapti</h1>
        <p>Telefon brauzerida ochildi</p>
    </body>
    </html>
    """

