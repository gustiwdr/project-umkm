"""
Entry point aplikasi (mode CLI).
Digunakan untuk pengujian logic sebelum GUI.
"""

from services.transaksi_service import transaksi_pembelian, transaksi_penjualan
from services.barang_service import get_all_barang
from services.laporan_service import *

if __name__ == "__main__":
    print("STOK AKHIR")
    print(get_stok_akhir())

    laba_barang, total = hitung_laba()
    print("\nLABA PER BARANG:", laba_barang)
    print("TOTAL LABA:", total)

    print("\nBARANG TERLARIS:", barang_terlaris())
    print("STOK TERENDAH:", barang_stok_terendah())

    print("\nPERINGATAN STOK:")
    print(peringatan_stok_minimum())

