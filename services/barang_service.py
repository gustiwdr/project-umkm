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

def update_barang(kode, data_baru):
    """
    Mengubah data barang berdasarkan kode.
    """
    data = load_csv(DATA_BARANG_FILE)
    ditemukan = False

    for item in data:
        if item["kode"] == kode:
            item.update(data_baru)
            ditemukan = True
            break

    if not ditemukan:
        raise ValueError("Barang tidak ditemukan")

    save_csv(DATA_BARANG_FILE, FIELDNAMES, data)

def hapus_barang(kode):
    """
    Menghapus data barang berdasarkan kode.
    """
    data = load_csv(DATA_BARANG_FILE)
    data_baru = [item for item in data if item["kode"] != kode]

    if len(data) == len(data_baru):
        raise ValueError("Barang tidak ditemukan")

    save_csv(DATA_BARANG_FILE, FIELDNAMES, data_baru)

