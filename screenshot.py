import os
import time
import base64
import boto3
from io import BytesIO
from flask import Flask, request, send_file, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Flask App
app = Flask(__name__)

# AWS S3 Konfiguration
S3_BUCKET_NAME = "screenshot-bucket-e340af8a"
s3_client = boto3.client("s3")

s3_client = boto3.client(
    "s3",
    aws_access_key_id="xxxx",
    aws_secret_access_key="xxxx",
    region_name="us-east-1"
)

# Sicherstellen, dass das temporäre Benutzerverzeichnis existiert
CHROME_USER_DIR = "/tmp/chrome-user-data"
os.makedirs(CHROME_USER_DIR, exist_ok=True)

# Chrome Optionen setzen
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(f"--user-data-dir={CHROME_USER_DIR}")

# ChromeDriver Pfad
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"

@app.route('/screenshot', methods=['GET'])
def take_screenshot():
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "URL Parameter fehlt"}), 400

    # ChromeDriver starten
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(3)  # Wartezeit für Rendering
        
        # Berechne die vollständige Höhe der Seite
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, total_height)  # Fenstergröße anpassen

        # Screenshot aufnehmen
        screenshot = driver.get_screenshot_as_png()
        driver.quit()
        
        # Screenshot in S3 hochladen
        screenshot_filename = f"screenshot_{int(time.time())}.png"
        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=screenshot_filename, Body=screenshot, ContentType='image/png')
        
        # Generiere eine signierte URL (gültig für 24 Stunden)
        signed_url = s3_client.generate_presigned_url('get_object',
                                                      Params={'Bucket': S3_BUCKET_NAME, 'Key': screenshot_filename},
                                                      ExpiresIn=86400)  # 24 Stunden gültig
        
        return jsonify({"message": "Screenshot erfolgreich gespeichert", "s3_url": signed_url, "filename": screenshot_filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

