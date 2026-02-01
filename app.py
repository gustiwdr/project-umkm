"""
Entry point aplikasi (mode CLI).
Digunakan untuk pengujian logic sebelum GUI.
"""

from services.transaksi_service import transaksi_pembelian, transaksi_penjualan
from services.barang_service import get_all_barang
from services.laporan_service import *

if __name__ == "__main__":
    print(get_stok_akhir())

    laba_barang, total = hitung_laba()
    print("\nLaba per barang:", laba_barang)
    print("\nTotal laba:", total)

    print("\nBarang terlaris:", barang_terlaris())
    print("\nStok terendah:", barang_stok_terendah().kode)

    print("\nPeringatan stok:", peringatan_stok_minimum())
