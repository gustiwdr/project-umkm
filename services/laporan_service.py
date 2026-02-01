"""
Modul ini berisi fungsi analisis
untuk pengambilan keputusan.
"""

from utils.file_handler import load_csv
from config import DATA_BARANG_FILE, DATA_TRANSAKSI_FILE, STOK_MINIMUM

def status_stok(stok):
    """
    Menentukan status stok berdasarkan batas minimum.
    """
    if stok == 0:
        return "Stok Habis"
    elif stok <= STOK_MINIMUM:
        return "Stok Menipis"
    else:
        return "Stok Aman"
    
def get_stok_akhir():
    """
    Menghitung stok akhir berdasarkan data transaksi.
    """
    barang_list = load_csv(DATA_BARANG_FILE)
    hasil = []

    for barang in barang_list:
        hasil.append({
            "kode": barang["kode"],
            "nama": barang["nama"],
            "stok": int(barang["stok"]),
            "status": status_stok(int(barang["stok"]))
        })
    
    return hasil

def hitung_laba():
    """
    Menghitung laba per barang dan total laba dari seluruh transaksi penjualan.
    """
    barang_list = load_csv(DATA_BARANG_FILE)
    transaksi_list = load_csv(DATA_TRANSAKSI_FILE)

    # Mapping barang berdasarkan kode
    barang_map = {}
    for b in barang_list:
        barang_map[b["kode"]] = b

    laba_per_barang = {}
    total_laba = 0

    for trx in transaksi_list:
        if trx["jenis"] == "penjualan":
            kode = trx["kode_barang"]
            jumlah = int(trx["jumlah"])

            harga_beli = int(barang_map[kode]["harga_beli"])
            harga_jual = int(barang_map[kode]["harga_jual"])

            laba = (harga_jual - harga_beli) * jumlah

            laba_per_barang[kode] = laba_per_barang.get(kode, 0) + laba
            total_laba += laba

    return laba_per_barang, total_laba

def barang_terlaris():
    """
    Menentukan barang terlaris berdasarkan data transaksi penjualan.
    """
    transaksi_list = load_csv(DATA_TRANSAKSI_FILE)
    penjualan = {}

    for trx in transaksi_list:
        if trx["jenis"] == "penjualan":
            kode = trx["kode_barang"]
            penjualan[kode] = penjualan.get(kode, 0) + int(trx["jumlah"])

    if not penjualan:
        return None

    return max(penjualan, key=penjualan.get)

def barang_stok_terendah():
    """
    Menentukan barang dengan stok terendah.
    """
    barang_list = load_csv(DATA_BARANG_FILE)

    if not barang_list:
        return None

    return min(barang_list, key=lambda b: int(b["stok"]))

def peringatan_stok_minimum():
    """
    Mendapatkan daftar barang yang stoknya di bawah atau sama dengan batas minimum.
    """
    barang_list = load_csv(DATA_BARANG_FILE)
    peringatan = []

    for barang in barang_list:
        if int(barang["stok"]) <= STOK_MINIMUM:
            peringatan.append({
                "kode": barang["kode"],
                "nama": barang["nama"],
                "stok": int(barang["stok"])
            })

    return peringatan
