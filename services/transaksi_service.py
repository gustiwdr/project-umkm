"""
Modul ini menangani pencatatan transaksi
penjualan dan pembelian barang.
"""

from utils.file_handler import load_csv, save_csv
from utils.validator import validate_positive_number
from config import DATA_TRANSAKSI_FILE, DATA_BARANG_FILE
from models.barang import Barang
from models.transaksi import Transaksi

# Struktur kolom file transaksi
TRANSAKSI_FIELDS = [
    "kode_transaksi",
    "tanggal",
    "jenis",
    "kode_barang",
    "jumlah"
]

BARANG_FIELDS = ["kode", "nama", "harga_beli", "harga_jual", "stok"]

def generate_kode_transaksi():
    """
    Menghasilkan kode transaksi otomatis
    berdasarkan transaksi terakhir.
    Format: TRX001, TRX002, dst.
    """
    transaksi_list = load_csv(DATA_TRANSAKSI_FILE)

    if not transaksi_list:
        return "TRX001"

    last_kode = transaksi_list[-1]["kode_transaksi"]
    nomor = int(last_kode.replace("TRX", ""))
    return f"TRX{nomor + 1:03d}"

def transaksi_pembelian(tanggal, kode_barang, jumlah):
    """
    Melakukan transaksi pembelian barang.
    Stok barang akan bertambah sesuai jumlah pembelian.
    """

    # Validasi jumlah pembelian
    validate_positive_number(jumlah, "Jumlah Pembelian")

    kode_transaksi = generate_kode_transaksi()

    # Ambil data transaksi yang sudah ada
    transaksi_list = load_csv(DATA_TRANSAKSI_FILE)

    # Cek apakah kode transaksi sudah ada
    for trx in transaksi_list:
        if trx["kode_transaksi"] == kode_transaksi:
            raise ValueError("Kode transaksi sudah terdaftar")

    # Ambil data barang
    barang_list = load_csv(DATA_BARANG_FILE)
    barang_ditemukan = False

    # Update stok barang
    for i, data in enumerate(barang_list):
        if data["kode"] == kode_barang:
            barang_obj = Barang(**data)
            barang_obj.tambah_stok(jumlah)

            # kembalikan ke bentuk dict untuk CSV
            barang_list[i] = barang_obj.to_dict()
            barang_ditemukan = True
            break


    # Jika barang tidak ditemukan
    if not barang_ditemukan:
        raise ValueError("Kode barang tidak ditemukan")

    # Simpan perubahan stok barang
    save_csv(DATA_BARANG_FILE, BARANG_FIELDS, barang_list)

    # Catat/simpan transaksi pembelian
    trx = Transaksi(
        kode_transaksi,
        tanggal,
        "pembelian",
        kode_barang,
        jumlah
    )
    simpan_transaksi(trx.to_dict())

def transaksi_penjualan(tanggal, kode_barang, jumlah):
    """
    Melakukan transaksi penjualan barang.
    Stok barang akan berkurang sesuai jumlah penjualan.
    """

    # Validasi jumlah penjualan
    validate_positive_number(jumlah, "Jumlah Penjualan")

    kode_transaksi = generate_kode_transaksi()

    # Ambil data transaksi yang sudah ada
    transaksi_list = load_csv(DATA_TRANSAKSI_FILE)

    # Cek apakah kode transaksi sudah ada
    for trx in transaksi_list:
        if trx["kode_transaksi"] == kode_transaksi:
            raise ValueError("Kode transaksi sudah terdaftar")

    # Ambil data barang
    barang_list = load_csv(DATA_BARANG_FILE)
    barang_ditemukan = False

    # Update stok barang
    for i, data in enumerate(barang_list):
        if data["kode"] == kode_barang:
            barang_obj = Barang(**data)
            barang_obj.kurangi_stok(jumlah)
            barang_list[i] = barang_obj.to_dict()
            barang_ditemukan = True
            break

    # Jika barang tidak ditemukan
    if not barang_ditemukan:
        raise ValueError("Kode barang tidak ditemukan")

    # Simpan perubahan stok barang
    save_csv(DATA_BARANG_FILE, BARANG_FIELDS, barang_list)

    # Catat/simpan transaksi penjualan
    trx = Transaksi(
        kode_transaksi,
        tanggal,
        "penjualan",
        kode_barang,
        jumlah
    )
    simpan_transaksi(trx.to_dict())

def simpan_transaksi(transaksi):
    """
    Menyimpan satu transaksi ke file CSV.
    """
    data = load_csv(DATA_TRANSAKSI_FILE)
    data.append(transaksi)
    save_csv(DATA_TRANSAKSI_FILE, TRANSAKSI_FIELDS, data)
