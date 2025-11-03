from sqlalchemy import text
from config.database import engine

with engine.connect() as conn:
    print("🔧 Menyesuaikan sequence auto increment untuk kolom 'id_pengguna'...")

    # Perbarui sequence sesuai nilai maksimum id_pengguna saat ini
    conn.execute(text("""
        SELECT setval(
            pg_get_serial_sequence('pengguna', 'id_pengguna'),
            COALESCE((SELECT MAX(id_pengguna) FROM pengguna), 1)
        );
    """))

    conn.commit()
    print("✅ Sequence untuk kolom 'id_pengguna' telah disinkronkan!")
