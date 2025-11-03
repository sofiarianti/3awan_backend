from flask import jsonify, request
from config.database import get_db
from models.menu_model import Menu
from models.kategory_model import Kategori
from sqlalchemy.orm import Session
from sqlalchemy import join

def get_all_menu():
    db: Session = next(get_db())
    data = db.query(Menu).all()
    return jsonify([{
        "id_menu": m.id_menu,
        "nama_makanan": m.nama_makanan,
        "id_kategori": m.id_kategori,
        "harga": m.harga,
        "deskripsi": m.deskripsi,
        "image_url": m.image_url
    } for m in data])


def add_menu():
    db: Session = next(get_db())
    body = request.json

    new_data = Menu(
        nama_makanan=body["nama_makanan"],
        id_kategori=body["id_kategori"],
        harga=body["harga"],
        deskripsi=body["deskripsi"],
        image_url=body["image_url"]
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return jsonify({
        "message": "Data menu berhasil ditambahkan",
        "data": {
            "id_menu": new_data.id_menu,
            "nama_makanan": new_data.nama_makanan,
            "id_kategori": new_data.id_kategori,
            "harga": new_data.harga,
            "deskripsi": new_data.deskripsi,
            "image_url": new_data.image_url
        }
    })

def update_menu(id_menu):
    db: Session = next(get_db())
    body = request.json

    menu = db.query(Menu).filter(Menu.id_menu == id_menu).first()
    if not menu:
        return jsonify({"message": "Menu tidak ditemukan"}), 404

    menu.nama_makanan = body.get("nama_makanan", menu.nama_makanan)
    menu.id_kategori = body.get("id_kategori", menu.id_kategori)
    menu.harga = body.get("harga", menu.harga)
    menu.deskripsi = body.get("deskripsi", menu.deskripsi)
    menu.image_url = body.get("image_url", menu.image_url)

    db.commit()
    db.refresh(menu)

    return jsonify({
        "message": "Data menu berhasil diperbarui",
        "data": {
            "id_menu": menu.id_menu,
            "nama_makanan": menu.nama_makanan,
            "id_kategori": menu.id_kategori,
            "harga": menu.harga,
            "deskripsi": menu.deskripsi,
            "image_url": menu.image_url
        }
    }), 200

def delete_menu(id_menu):
    db: Session = next(get_db())
    menu = db.query(Menu).filter(Menu.id_menu == id_menu).first()
    if not menu:
        return jsonify({"message": "Menu tidak ditemukan"}), 404

    db.delete(menu)
    db.commit()

    return jsonify({"message": f"Data menu dengan id {id_menu} berhasil dihapus"}), 200

def get_menu_by_kategori(id_kategori):
    db: Session = next(get_db())

    # inner join Menu <-> Kategori on id_kategori
    q = db.query(Menu, Kategori).join(Kategori, Menu.id_kategori == Kategori.id_kategori).filter(Menu.id_kategori == id_kategori)
    results = q.all()

    # results is list of tuples (Menu, Kategori)
    return jsonify([{
        "id_menu": m.id_menu,
        "nama_makanan": m.nama_makanan,
        "id_kategori": m.id_kategori,
        "kategori": k.kategori,
        "harga": m.harga,
        "deskripsi": m.deskripsi,
        "image_url": m.image_url
    } for (m, k) in results])