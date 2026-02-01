"""
Modul ini menangani seluruh logic
yang berkaitan dengan data barang (CRUD).
"""

from utils.file_handler import load_csv, save_csv
from utils.validator import validate_not_empty, validate_positive_number
from config import DATA_BARANG_FILE
from models.barang import Barang

# Struktur kolom file barang
FIELDNAMES = ["kode", "nama", "harga_beli", "harga_jual", "stok"]

def get_all_barang():
    """
    Mengambil seluruh data barang dari file CSV.
    """
    return load_csv(DATA_BARANG_FILE)


def tambah_barang(barang_data):
    """
    Menambahkan data barang baru ke sistem.
    """
    # Validasi input
    validate_not_empty(barang_data["kode"], "Kode Barang")
    validate_not_empty(barang_data["nama"], "Nama Barang")
    validate_positive_number(barang_data["stok"], "Stok")

    # Ambil data lama
    data = get_all_barang()

    # Cek apakah kode barang sudah ada
    for item in data:
        if item["kode"] == barang_data["kode"]:
            raise ValueError("Kode barang sudah terdaftar")

    # Buat object Barang (OOP)
    barang_obj = Barang(**barang_data)

    # Simpan sebagai dict ke CSV
    data.append(barang_obj.to_dict())

    # Simpan kembali ke file
    save_csv(DATA_BARANG_FILE, FIELDNAMES, data)
