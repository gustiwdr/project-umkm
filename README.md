# Sistem Manajemen Penjualan dan Stok UMKM

## Deskripsi

Aplikasi desktop berbasis Python yang digunakan untuk mengelola data barang,
mencatat transaksi pembelian dan penjualan, serta menyajikan laporan stok dan
analisis sederhana untuk mendukung pengambilan keputusan pada UMKM ritel.

## Fitur Utama

- Manajemen data barang (tambah, ubah, hapus, tampil)
- Transaksi pembelian dan penjualan barang
- Pembaruan stok otomatis
- Laporan stok akhir dan status stok
- Ekspor laporan ke format CSV dan PDF
- Antarmuka pengguna berbasis GUI (Tkinter)

## Struktur Folder

```
project-umkm/
│
├── data/ # Dataset CSV
├── gui/ # Antarmuka pengguna (Tkinter)
├── models/ # Class OOP (Barang, Transaksi)
├── services/ # Logika bisnis aplikasi
├── utils/ # Utility (file handler, validator)
├── app.py # Entry point aplikasi
├── cli_app.py # Versi CLI aplikasi
├── config.py # Konfigurasi aplikasi
└── README.md
```

## Cara Menjalankan Aplikasi

1. Pastikan Python 3.x telah terinstal
2. Install dependensi:
   ```bash
    pip install tkcalendar
    pip install reportlab
   ```
3. Jalankan aplikasi:
   ```bash
    python3 app.py
   ```

## Dataset

Dataset disimpan dalam folder data/ dengan format CSV:

- barang.csv
- transaksi.csv

## Catatan

Seluruh logika bisnis dipisahkan dari antarmuka pengguna untuk menjaga keterbacaan, modularitas, dan kemudahan pengembangan aplikasi.
