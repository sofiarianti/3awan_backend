from flask import jsonify, request
from config.database import get_db
from models.kategory_model import Kategori
from sqlalchemy.orm import Session
from datetime import datetime

def get_all_kategori():
    db: Session = next(get_db())
    data = db.query(Kategori).all()
    return jsonify([{
        "id_kategori": k.id_kategori,
        "kategori": k.kategori,
    } for k in data])

def add_kategori():  
    db: Session = next(get_db())
    body = request.json

    # Jangan terima atau set id_kategori dari client - biarkan DB yang mengisi secara otomatis
    new_data = Kategori(
        kategori=body["kategori"],
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return jsonify({
        "message": "Data berhasil ditambahkan",
        "id_kategori": new_data.id_kategori,
        "kategori": new_data.kategori,
    })

def update_kategori(id_kategori):
    db: Session = next(get_db())
    body = request.json

    kategori = db.query(Kategori).filter(Kategori.id_kategori == id_kategori).first()
    if not kategori:
        return jsonify({"message": "Wisata tidak ditemukan"}), 404

    # Update field sesuai data yang dikirim
    kategori.kategori = body.get("kategori", kategori.kategori)

    db.commit()
    db.refresh(kategori)

    return jsonify({
        "message": "Data berhasil diperbarui",
        "data": {
            "id_katrgori": kategori.id_kategori,
            "kategori": kategori.kategori,
        }
    }), 200

def delete_kategori(id_kategori):
    db: Session = next(get_db())
    kategori = db.query(Kategori).filter(Kategori.id_kategori == id_kategori).first()
    if not kategori:
        return jsonify({"message": "Wisata tidak ditemukan"}), 404

    db.delete(kategori)
    db.commit()

    return jsonify({"message": f"Data kategori dengan id {id_kategori} berhasil dihapus"}), 200