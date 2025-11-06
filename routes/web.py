from flask import Blueprint
from controllers.kategori_controller import get_all_kategori, add_kategori, update_kategori, delete_kategori
from controllers.menu_controller import get_all_menu, add_menu, update_menu, delete_menu, get_menu_by_kategori
from controllers.user_controller import get_all_users, add_user, update_user, delete_user
from controllers.pembayaran_controller import get_all_pembayaran, add_pembayaran, update_pembayaran, delete_pembayaran

web = Blueprint("web", __name__)

# Menu routes
web.route("/", methods=["GET"])(get_all_menu)
web.route("/menu/insert", methods=["POST"])(add_menu)
web.route("/menu/update/<int:id_menu>", methods=["PUT"])(update_menu)
web.route("/menu/delete/<int:id_menu>", methods=["DELETE"])(delete_menu)
web.route("/menu/kategori/<int:id_kategori>", methods=["GET"])(get_menu_by_kategori)

# Kategori routes
web.route("/kategori", methods=["GET"])(get_all_kategori)
web.route("/kategori/insert", methods=["POST"])(add_kategori)
web.route("/kategori/update/<int:id_kategori>", methods=["PUT"])(update_kategori)
web.route("/kategori/delete/<int:id_kategori>", methods=["DELETE"])(delete_kategori)

# User routes
web.route("/users", methods=["GET"])(get_all_users)
web.route("/users/insert", methods=["POST"])(add_user)
web.route("/users/update/<int:id_pengguna>", methods=["PUT"])(update_user)
web.route("/users/delete/<int:id_pengguna>", methods=["DELETE"])(delete_user)

# Pembayaran routes
web.route("/pembayaran", methods=["GET"])(get_all_pembayaran)
web.route("/pembayaran/insert", methods=["POST"])(add_pembayaran)
web.route("/pembayaran/update/<int:id_pembayaran>", methods=["PUT"])(update_pembayaran)
web.route("/pembayaran/delete/<int:id_pembayaran>", methods=["DELETE"])(delete_pembayaran)