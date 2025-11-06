from sqlalchemy import text
from config.database import engine

with engine.connect() as conn:
    print("🗑️ Menghapus tabel 'pemesanan' jika ada...")

    # Hapus tabel 'pemesanan' jika sudah ada di database
    conn.execute(text("""
        DROP TABLE IF EXISTS pemesanan;
    """))

    conn.commit()
    print("✅ Tabel 'pemesanan' berhasil dihapus (atau tidak ada sebelumnya)!")
