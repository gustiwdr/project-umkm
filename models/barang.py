"""
Class Barang merepresentasikan satu barang dalam sistem
dan menyediakan method terkait stok dan harga.
"""

class Barang:
    def __init__(self, kode, nama, harga_beli, harga_jual, stok):
        self.kode = kode
        self.nama = nama
        self.harga_beli = int(harga_beli)
        self.harga_jual = int(harga_jual)
        self.stok = int(stok)

    def tambah_stok(self, jumlah):
        """
        Menambah stok barang (pembelian).
        """
        if jumlah <= 0:
            raise ValueError("Jumlah pembelian harus lebih dari 0")
        self.stok += jumlah

    def kurangi_stok(self, jumlah):
        """
        Mengurangi stok barang (penjualan).
        """
        if jumlah <= 0:
            raise ValueError("Jumlah penjualan harus lebih dari 0")
        if self.stok < jumlah:
            raise ValueError("Stok tidak mencukupi")
        self.stok -= jumlah

    def hitung_laba(self, jumlah_terjual):
        """
        Menghitung laba berdasarkan jumlah terjual.
        """
        return (self.harga_jual - self.harga_beli) * jumlah_terjual

    def to_dict(self):
        """
        Mengubah objek Barang ke dictionary
        agar kompatibel dengan CSV.
        """
        return {
            "kode": self.kode,
            "nama": self.nama,
            "harga_beli": self.harga_beli,
            "harga_jual": self.harga_jual,
            "stok": self.stok
        }
