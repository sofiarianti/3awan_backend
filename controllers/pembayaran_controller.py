from flask import jsonify, request
from config.database import get_db
from models.pembayaran_model import Pembayaran
from sqlalchemy.orm import Session

def get_all_pembayaran():
    db: Session = next(get_db())
    data = db.query(Pembayaran).all()
    return jsonify([{
        "id_pembayaran": p.id_pembayaran,
        "id_pemesanan": p.id_pemesanan,
        "id_pengguna": p.id_pengguna,
        "id_menu": p.id_menu,
        "id_kategori": p.id_kategori,
        "metode_pembayaran": p.metode_pembayaran,
        "qr_code_url": p.qr_code_url,
        "status": p.status
    } for p in data])

def add_pembayaran():
    db: Session = next(get_db())
    body = request.json

    new_data = Pembayaran(
        id_pemesanan=body["id_pemesanan"],
        id_pengguna=body["id_pengguna"],
        id_menu=body["id_menu"],
        id_kategori=body["id_kategori"],
        metode_pembayaran=body["metode_pembayaran"],
        qr_code_url=body["qr_code_url"],
        status=body["status"]
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return jsonify({
        "message": "Data pembayaran berhasil ditambahkan",
        "data": {
            "id_pembayaran": new_data.id_pembayaran,
            "id_pemesanan": new_data.id_pemesanan,
            "id_pengguna": new_data.id_pengguna,
            "id_menu": new_data.id_menu,
            "id_kategori": new_data.id_kategori,
            "metode_pembayaran": new_data.metode_pembayaran,
            "qr_code_url": new_data.qr_code_url,
            "status": new_data.status
        }
    })

def update_pembayaran(id_pembayaran):
    db: Session = next(get_db())
    body = request.json

    pembayaran = db.query(Pembayaran).filter(Pembayaran.id_pembayaran == id_pembayaran).first()
    if not pembayaran:
        return jsonify({"message": "Pembayaran tidak ditemukan"}), 404

    pembayaran.id_pemesanan = body.get("id_pemesanan", pembayaran.id_pemesanan)
    pembayaran.id_pengguna = body.get("id_pengguna", pembayaran.id_pengguna)
    pembayaran.id_menu = body.get("id_menu", pembayaran.id_menu)
    pembayaran.id_kategori = body.get("id_kategori", pembayaran.id_kategori)
    pembayaran.metode_pembayaran = body.get("metode_pembayaran", pembayaran.metode_pembayaran)
    pembayaran.qr_code_url = body.get("qr_code_url", pembayaran.qr_code_url)
    pembayaran.status = body.get("status", pembayaran.status)

    db.commit()
    db.refresh(pembayaran)

    return jsonify({
        "message": "Data pembayaran berhasil diperbarui",
        "data": {
            "id_pembayaran": pembayaran.id_pembayaran,
            "id_pemesanan": pembayaran.id_pemesanan,
            "id_pengguna": pembayaran.id_pengguna,
            "id_menu": pembayaran.id_menu,
            "id_kategori": pembayaran.id_kategori,
            "metode_pembayaran": pembayaran.metode_pembayaran,
            "qr_code_url": pembayaran.qr_code_url,
            "status": pembayaran.status
        }
    }), 200

def delete_pembayaran(id_pembayaran):
    db: Session = next(get_db())
    pembayaran = db.query(Pembayaran).filter(Pembayaran.id_pembayaran == id_pembayaran).first()
    if not pembayaran:
        return jsonify({"message": "Pembayaran tidak ditemukan"}), 404

    db.delete(pembayaran)
    db.commit()

    return jsonify({"message": f"Data pembayaran dengan id {id_pembayaran} berhasil dihapus"}), 200