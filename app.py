from flask import Flask
from flask_cors import CORS
from config.database import engine, Base
from routes.web import web
import models.kategory_model  # register model
import os  # untuk ambil PORT dari Railway

# Inisialisasi Flask
app = Flask(__name__)
CORS(app)

# Buat tabel otomatis kalau belum ada
Base.metadata.create_all(bind=engine)

# Daftarkan blueprint routes
app.register_blueprint(web)

# HANYA untuk testing lokal (Railway akan jalankan lewat Gunicorn)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
