from sqlalchemy import text
from config.database import engine

with engine.connect() as conn:
    print("🔧 Menambahkan kolom 'role' ke tabel 'pengguna'...")

    # Tambahkan kolom 'role' jika belum ada
    conn.execute(text("""
        ALTER TABLE pengguna
        ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'user';
    """))

    conn.commit()
    print("✅ Kolom 'role' berhasil ditambahkan (atau sudah ada sebelumnya)!")
