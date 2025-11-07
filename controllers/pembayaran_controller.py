from flask import jsonify, request
from config.database import get_db
from models.pembayaran_model import Pembayaran
from models.user_model import Pengguna
from models.menu_model import Menu
from models.kategory_model import Kategori
from sqlalchemy.orm import Session
import qrcode
import os


def generate_qr_code_url(data, id_pembayaran):
    """
    Generate QR code and save it as a file
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    if not os.path.exists("qrcodes"):
        os.makedirs("qrcodes")
    file_path = f"qrcodes/pembayaran_{id_pembayaran}.png"
    img.save(file_path)

    return file_path


def get_all_pembayaran():
    db: Session = next(get_db())
    # Inner join dengan tabel pengguna, menu, dan kategori
    data = db.query(
        Pembayaran,
        Pengguna.nama,
        Menu.nama_makanan,
        Kategori.kategori
    ).join(
        Pengguna, Pembayaran.id_pengguna == Pengguna.id_pengguna
    ).join(
        Menu, Pembayaran.id_menu == Menu.id_menu
    ).join(
        Kategori, Pembayaran.id_kategori == Kategori.id_kategori
    ).all()

    return jsonify([{
        "id_pembayaran": p.id_pembayaran,
        "nama_pengguna": nama,
        "nama_menu": nama_makanan,
        "kategori": kategori,
        "jumlah": p.jumlah,
        "metode_pembayaran": p.metode_pembayaran,
        "qr_code_url": p.qr_code_url,
        "status": p.status,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None
    } for p, nama, nama_makanan, kategori in data])


def add_pembayaran():
    db: Session = next(get_db())
    body = request.json

    required_fields = ["id_pengguna", "id_menu", "id_kategori", "jumlah", "metode_pembayaran", "status"]
    for field in required_fields:
        if field not in body:
            return jsonify({"message": f"Field {field} harus diisi"}), 400

    new_data = Pembayaran(
        id_pengguna=body["id_pengguna"],
        id_menu=body["id_menu"],
        id_kategori=body["id_kategori"],
        jumlah=body["jumlah"],
        metode_pembayaran=body["metode_pembayaran"],
        status=body["status"]
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    # Ambil data lengkap setelah disimpan
    joined_data = (
        db.query(
            Pembayaran,
            Pengguna.nama,
            Menu.nama_makanan,
            Kategori.kategori
        )
        .join(Pengguna, Pembayaran.id_pengguna == Pengguna.id_pengguna)
        .join(Menu, Pembayaran.id_menu == Menu.id_menu)
        .join(Kategori, Pembayaran.id_kategori == Kategori.id_kategori)
        .filter(Pembayaran.id_pembayaran == new_data.id_pembayaran)
        .first()
    )

    # Buat isi QR code dari hasil join
    if joined_data:
        pembayaran, nama_pengguna, nama_menu, kategori = joined_data
        qr_data = (
            f"ID Pembayaran: {pembayaran.id_pembayaran}\n"
            f"Nama Pengguna: {nama_pengguna}\n"
            f"Menu: {nama_menu}\n"
            f"Kategori: {kategori}\n"
            f"Jumlah: {pembayaran.jumlah}\n"
            f"Metode: {pembayaran.metode_pembayaran}\n"
            f"Status: {pembayaran.status}\n"
            f"Tanggal: {pembayaran.created_at}"
        )

        # Generate QR code dengan data lengkap
        new_data.qr_code_url = generate_qr_code_url(qr_data, new_data.id_pembayaran)
        db.commit()
        db.refresh(new_data)

    return jsonify({
        "message": "Data pembayaran berhasil ditambahkan",
        "data": {
            "id_pembayaran": new_data.id_pembayaran,
            "id_pengguna": new_data.id_pengguna,
            "id_menu": new_data.id_menu,
            "id_kategori": new_data.id_kategori,
            "jumlah": new_data.jumlah,
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

    # Update data pembayaran
    pembayaran.id_pengguna = body.get("id_pengguna", pembayaran.id_pengguna)
    pembayaran.id_menu = body.get("id_menu", pembayaran.id_menu)
    pembayaran.id_kategori = body.get("id_kategori", pembayaran.id_kategori)
    pembayaran.jumlah = body.get("jumlah", pembayaran.jumlah)
    pembayaran.metode_pembayaran = body.get("metode_pembayaran", pembayaran.metode_pembayaran)
    pembayaran.status = body.get("status", pembayaran.status)

    # Generate QR code baru
    qr_data = f"ID_Pembayaran:{pembayaran.id_pembayaran}_Pengguna:{pembayaran.id_pengguna}_Menu:{pembayaran.id_menu}_Jumlah:{pembayaran.jumlah}_Metode:{pembayaran.metode_pembayaran}"
    pembayaran.qr_code_url = generate_qr_code_url(qr_data, pembayaran.id_pembayaran)

    db.commit()
    db.refresh(pembayaran)

    return jsonify({
        "message": "Data pembayaran berhasil diperbarui",
        "data": {
            "id_pembayaran": pembayaran.id_pembayaran,
            "id_pengguna": pembayaran.id_pengguna,
            "id_menu": pembayaran.id_menu,
            "id_kategori": pembayaran.id_kategori,
            "jumlah": pembayaran.jumlah,
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
