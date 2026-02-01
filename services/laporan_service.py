"""
Modul ini berisi fungsi analisis
untuk pengambilan keputusan.
"""

from utils.file_handler import load_csv
from config import DATA_BARANG_FILE, DATA_TRANSAKSI_FILE, STOK_MINIMUM
from models.barang import Barang

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
    
def _load_barang_objects():
    """
    Helper function:
    Mengubah data barang dari CSV menjadi objek Barang.
    """
    barang_list = load_csv(DATA_BARANG_FILE)
    objects = []

    for data in barang_list:
        objects.append(Barang(**data))

    return objects
    
def get_stok_akhir():
    """
    Menghitung stok akhir berdasarkan data transaksi.
    """
    barang_objects = _load_barang_objects()
    hasil = []

    for barang in barang_objects:
        hasil.append({
            "kode": barang.kode,
            "nama": barang.nama,
            "stok": barang.stok,
            "status": status_stok(barang.stok)
        })
    
    return hasil

def hitung_laba():
    """
    Menghitung laba per barang dan total laba dari seluruh transaksi penjualan.
    """
    barang_objects = _load_barang_objects()
    transaksi_list = load_csv(DATA_TRANSAKSI_FILE)

    # Mapping barang berdasarkan kode
    barang_map = {barang.kode: barang for barang in barang_objects}

    laba_per_barang = {}
    total_laba = 0

    for trx in transaksi_list:
        if trx["jenis"] == "penjualan":
            kode = trx["kode_barang"]
            jumlah = int(trx["jumlah"])

            barang = barang_map.get(kode)
            if not barang:
                continue

            laba = barang.hitung_laba(jumlah)

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
    barang_objects = _load_barang_objects()

    if not barang_objects:
        return None

    return min(barang_objects, key=lambda b: b.stok)

def peringatan_stok_minimum():
    """
    Mendapatkan daftar barang yang stoknya di bawah atau sama dengan batas minimum.
    """
    barang_objects = _load_barang_objects()
    peringatan = []

    for barang in barang_objects:
        if barang.stok <= STOK_MINIMUM:
            peringatan.append({
                "kode": barang.kode,
                "nama": barang.nama,
                "stok": barang.stok
            })

    return peringatan
