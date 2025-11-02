from flask import jsonify, request
from config.database import get_db
from models.pemesanan_model import Pemesanan
from sqlalchemy.orm import Session

def get_all_pemesanan():
    db: Session = next(get_db())
    data = db.query(Pemesanan).all()
    return jsonify([{
        "id_pemesanan": p.id_pemesanan,
        "id_pengguna": p.id_pengguna,
        "id_menu": p.id_menu,
        "id_kategori": p.id_kategori,
        "jumlah": p.jumlah,
        "status": p.status
    } for p in data])

def add_pemesanan():
    db: Session = next(get_db())
    body = request.json

    new_data = Pemesanan(
        id_pengguna=body["id_pengguna"],
        id_menu=body["id_menu"],
        id_kategori=body["id_kategori"],
        jumlah=body["jumlah"],
        status=body["status"]
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return jsonify({
        "message": "Data pemesanan berhasil ditambahkan",
        "data": {
            "id_pemesanan": new_data.id_pemesanan,
            "id_pengguna": new_data.id_pengguna,
            "id_menu": new_data.id_menu,
            "id_kategori": new_data.id_kategori,
            "jumlah": new_data.jumlah,
            "status": new_data.status
        }
    })

def update_pemesanan(id_pemesanan):
    db: Session = next(get_db())
    body = request.json

    pemesanan = db.query(Pemesanan).filter(Pemesanan.id_pemesanan == id_pemesanan).first()
    if not pemesanan:
        return jsonify({"message": "Pemesanan tidak ditemukan"}), 404

    pemesanan.id_pengguna = body.get("id_pengguna", pemesanan.id_pengguna)
    pemesanan.id_menu = body.get("id_menu", pemesanan.id_menu)
    pemesanan.id_kategori = body.get("id_kategori", pemesanan.id_kategori)
    pemesanan.jumlah = body.get("jumlah", pemesanan.jumlah)
    pemesanan.status = body.get("status", pemesanan.status)

    db.commit()
    db.refresh(pemesanan)

    return jsonify({
        "message": "Data pemesanan berhasil diperbarui",
        "data": {
            "id_pemesanan": pemesanan.id_pemesanan,
            "id_pengguna": pemesanan.id_pengguna,
            "id_menu": pemesanan.id_menu,
            "id_kategori": pemesanan.id_kategori,
            "jumlah": pemesanan.jumlah,
            "status": pemesanan.status
        }
    }), 200

def delete_pemesanan(id_pemesanan):
    db: Session = next(get_db())
    pemesanan = db.query(Pemesanan).filter(Pemesanan.id_pemesanan == id_pemesanan).first()
    if not pemesanan:
        return jsonify({"message": "Pemesanan tidak ditemukan"}), 404

    db.delete(pemesanan)
    db.commit()

    return jsonify({"message": f"Data pemesanan dengan id {id_pemesanan} berhasil dihapus"}), 200