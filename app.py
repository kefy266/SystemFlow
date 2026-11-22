from pathlib import Path

from flask import Flask, send_from_directory


ROOT_DIR = Path(__file__).resolve().parent
WEB_DIR = ROOT_DIR / "app"

app = Flask(__name__)


@app.get("/")
def home():
    return send_from_directory(WEB_DIR, "index.html")


@app.get("/testler.html")
def testler():
    return send_from_directory(WEB_DIR, "testler.html")


@app.get("/veriler.json")
def veriler():
    return send_from_directory(ROOT_DIR, "veriler.json")


@app.get("/vtesteriler.json")
def test_verileri():
    return send_from_directory(ROOT_DIR, "vtesteriler.json")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8082)
