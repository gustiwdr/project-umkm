"""
Aplikasi CLI Sistem Manajemen UMKM
Digunakan untuk pengujian dan penggunaan via terminal.
"""

from services.barang_service import (
    get_all_barang,
    tambah_barang,
    update_barang,
    hapus_barang
)
from services.transaksi_service import (
    transaksi_pembelian,
    transaksi_penjualan
)
from services.laporan_service import (
    get_stok_akhir,
    hitung_laba,
    barang_terlaris,
    barang_stok_terendah,
    peringatan_stok_minimum
)
from services.export_service import (
    export_stok_to_csv,
    export_transaksi_to_csv
)


def menu():
    print("\n=== SISTEM MANAJEMEN UMKM (CLI) ===")
    print("1. Lihat Data Barang")
    print("2. Tambah Barang")
    print("3. Update Barang")
    print("4. Hapus Barang")
    print("5. Transaksi Pembelian")
    print("6. Transaksi Penjualan")
    print("7. Laporan Stok")
    print("8. Laporan Laba")
    print("9. Export Laporan")
    print("0. Keluar")


def lihat_barang():
    for b in get_all_barang():
        print(b)


def tambah_barang_cli():
    data = {
        "kode": input("Kode Barang: "),
        "nama": input("Nama Barang: "),
        "harga_beli": input("Harga Beli: "),
        "harga_jual": input("Harga Jual: "),
        "stok": input("Stok Awal: ")
    }
    tambah_barang(data)
    print("Barang berhasil ditambahkan")


def update_barang_cli():
    kode = input("Kode Barang: ")
    data = {
        "nama": input("Nama Baru: "),
        "harga_beli": input("Harga Beli Baru: "),
        "harga_jual": input("Harga Jual Baru: "),
        "stok": input("Stok Baru: ")
    }
    update_barang(kode, data)
    print("Barang berhasil diperbarui")


def hapus_barang_cli():
    kode = input("Kode Barang: ")
    hapus_barang(kode)
    print("Barang berhasil dihapus")


def pembelian_cli():
    tanggal = input("Tanggal (YYYY-MM-DD): ")
    kode = input("Kode Barang: ")
    jumlah = int(input("Jumlah: "))
    transaksi_pembelian(tanggal, kode, jumlah)
    print("Transaksi pembelian berhasil")


def penjualan_cli():
    tanggal = input("Tanggal (YYYY-MM-DD): ")
    kode = input("Kode Barang: ")
    jumlah = int(input("Jumlah: "))
    transaksi_penjualan(tanggal, kode, jumlah)
    print("Transaksi penjualan berhasil")


def laporan_stok():
    for b in get_stok_akhir():
        print(b)


def laporan_laba():
    laba, total = hitung_laba()
    print("Laba per barang:", laba)
    print("Total laba:", total)


def export_laporan():
    export_stok_to_csv()
    export_transaksi_to_csv()
    print("Laporan berhasil diekspor")


def main():
    while True:
        menu()
        pilihan = input("Pilih menu: ")

        try:
            if pilihan == "1":
                lihat_barang()
            elif pilihan == "2":
                tambah_barang_cli()
            elif pilihan == "3":
                update_barang_cli()
            elif pilihan == "4":
                hapus_barang_cli()
            elif pilihan == "5":
                pembelian_cli()
            elif pilihan == "6":
                penjualan_cli()
            elif pilihan == "7":
                laporan_stok()
            elif pilihan == "8":
                laporan_laba()
            elif pilihan == "9":
                export_laporan()
            elif pilihan == "0":
                print("Keluar dari aplikasi.")
                break
            else:
                print("Pilihan tidak valid")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
