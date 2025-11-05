from flask import jsonify, request
from config.database import get_db
from models.user_model import Pengguna
from sqlalchemy.orm import Session

def get_all_users():
    db: Session = next(get_db())
    data = db.query(Pengguna).all()
    return jsonify([{
        "id_pengguna": u.id_pengguna,
        "nama": u.nama,
        "email": u.email,
        "password": u.password,
        "role": u.role
    } for u in data])

def add_user():
    db: Session = next(get_db())
    body = request.json

    new_data = Pengguna(
        nama=body["nama"],
        email=body["email"],
        password=body["password"],
        role=body["role"]
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return jsonify({
        "message": "Data pengguna berhasil ditambahkan",
        "data": {
            "id_pengguna": new_data.id_pengguna,
            "nama": new_data.nama,
            "email": new_data.email,
            "role": new_data.role
        }
    })

def update_user(id_pengguna):
    db: Session = next(get_db())
    body = request.json

    user = db.query(Pengguna).filter(Pengguna.id_pengguna == id_pengguna).first()
    if not user:
        return jsonify({"message": "Pengguna tidak ditemukan"}), 404

    user.nama = body.get("nama", user.nama)
    user.email = body.get("email", user.email)
    user.password = body.get("password", user.password)
    user.role = body.get("role", user.role)

    db.commit()
    db.refresh(user)

    return jsonify({
        "message": "Data pengguna berhasil diperbarui",
        "data": {
            "id_pengguna": user.id_pengguna,
            "nama": user.nama,
            "email": user.email,
            "role": user.role
        }
    }), 200

def delete_user(id_pengguna):
    db: Session = next(get_db())
    user = db.query(Pengguna).filter(Pengguna.id_pengguna == id_pengguna).first()
    if not user:
        return jsonify({"message": "Pengguna tidak ditemukan"}), 404

    db.delete(user)
    db.commit()

    return jsonify({"message": f"Data pengguna dengan id {id_pengguna} berhasil dihapus"}), 200