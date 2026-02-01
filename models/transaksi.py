"""
Class Transaksi merepresentasikan satu transaksi
pembelian atau penjualan.
"""

class Transaksi:
    def __init__(self, kode_transaksi, tanggal, jenis, kode_barang, jumlah):
        self.kode_transaksi = kode_transaksi
        self.tanggal = tanggal
        self.jenis = jenis
        self.kode_barang = kode_barang
        self.jumlah = int(jumlah)

        self.validasi()

    def validasi(self):
        """
        Validasi data transaksi.
        """
        if self.jumlah <= 0:
            raise ValueError("Jumlah transaksi harus lebih dari 0")

        if self.jenis not in ["pembelian", "penjualan"]:
            raise ValueError("Jenis transaksi tidak valid")

    def to_dict(self):
        """
        Mengubah objek Transaksi ke dictionary
        untuk penyimpanan CSV.
        """
        return {
            "kode_transaksi": self.kode_transaksi,
            "tanggal": self.tanggal,
            "jenis": self.jenis,
            "kode_barang": self.kode_barang,
            "jumlah": self.jumlah
        }
