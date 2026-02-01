"""
Modul ini menangani pencatatan transaksi
penjualan dan pembelian barang.
"""

from utils.file_handler import load_csv, save_csv
from utils.validator import validate_positive_number
from config import DATA_TRANSAKSI_FILE, DATA_BARANG_FILE

# Struktur kolom file transaksi
TRANSAKSI_FIELDS = [
    "kode_transaksi",
    "tanggal",
    "jenis",
    "kode_barang",
    "jumlah"
]

BARANG_FIELDS = ["kode", "nama", "harga_beli", "harga_jual", "stok"]

def transaksi_pembelian(kode_transaksi, tanggal, kode_barang, jumlah):
    """
    Melakukan transaksi pembelian barang.
    Stok barang akan bertambah sesuai jumlah pembelian.
    """

    # Validasi jumlah pembelian
    validate_positive_number(jumlah, "Jumlah Pembelian")

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
    for barang in barang_list:
        if barang["kode"] == kode_barang:
            barang["stok"] = str(int(barang["stok"]) + jumlah)
            barang_ditemukan = True
            break

    # Jika barang tidak ditemukan
    if not barang_ditemukan:
        raise ValueError("Kode barang tidak ditemukan")

    # Simpan perubahan stok barang
    save_csv(DATA_BARANG_FILE, BARANG_FIELDS, barang_list)

    # Catat/simpan transaksi pembelian
    simpan_transaksi({
        "kode_transaksi": kode_transaksi,
        "tanggal": tanggal,
        "jenis": "pembelian",
        "kode_barang": kode_barang,
        "jumlah": jumlah
    })

def transaksi_penjualan(kode_transaksi, tanggal, kode_barang, jumlah):
    """
    Melakukan transaksi penjualan barang.
    Stok barang akan berkurang sesuai jumlah penjualan.
    """

    # Validasi jumlah penjualan
    validate_positive_number(jumlah, "Jumlah Penjualan")

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
    for barang in barang_list:
        if barang["kode"] == kode_barang:
            stok_sekarang = int(barang["stok"])

            # Cek stok cukup atau tidak
            if stok_sekarang < jumlah:
                raise ValueError("Stok barang tidak mencukupi untuk penjualan")

            # Kurangi stok
            barang["stok"] = str(stok_sekarang - jumlah)
            barang_ditemukan = True
            break

    # Jika barang tidak ditemukan
    if not barang_ditemukan:
        raise ValueError("Kode barang tidak ditemukan")

    # Simpan perubahan stok barang
    save_csv(DATA_BARANG_FILE, BARANG_FIELDS, barang_list)

    # Catat/simpan transaksi penjualan
    simpan_transaksi({
        "kode_transaksi": kode_transaksi,
        "tanggal": tanggal,
        "jenis": "penjualan",
        "kode_barang": kode_barang,
        "jumlah": jumlah
    })

def simpan_transaksi(transaksi):
    """
    Menyimpan satu transaksi ke file CSV.
    """
    data = load_csv(DATA_TRANSAKSI_FILE)
    data.append(transaksi)
    save_csv(DATA_TRANSAKSI_FILE, TRANSAKSI_FIELDS, data)
