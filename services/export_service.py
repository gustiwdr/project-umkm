"""
Modul ini menangani ekspor laporan
ke file CSV dan PDF.
"""

import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from services.laporan_service import get_stok_akhir
from utils.file_handler import load_csv
from config import DATA_TRANSAKSI_FILE

from services.laporan_service import get_stok_akhir


def export_stok_to_csv(filename="laporan_stok.csv"):
    """
    Mengekspor laporan stok barang ke file CSV.
    """
    data = get_stok_akhir()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Kode Barang", "Nama Barang", "Stok", "Status"])

        for item in data:
            writer.writerow([
                item["kode"],
                item["nama"],
                item["stok"],
                item["status"]
            ])


def export_stok_to_pdf(filename="laporan_stok.pdf"):
    """
    Mengekspor laporan stok barang ke file PDF.
    """
    data = get_stok_akhir()
    pdf = canvas.Canvas(filename, pagesize=A4)

    width, height = A4
    y = height - 50

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "LAPORAN STOK BARANG")
    y -= 30

    pdf.setFont("Helvetica", 10)

    # Header tabel
    pdf.drawString(50, y, "Kode")
    pdf.drawString(120, y, "Nama")
    pdf.drawString(300, y, "Stok")
    pdf.drawString(350, y, "Status")
    y -= 20

    for item in data:
        pdf.drawString(50, y, item["kode"])
        pdf.drawString(120, y, item["nama"])
        pdf.drawString(300, y, str(item["stok"]))
        pdf.drawString(350, y, item["status"])
        y -= 18

        # Pindah halaman jika penuh
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = height - 50

    pdf.save()

def export_transaksi_to_csv(jenis, filename):
    """
    Mengekspor laporan transaksi (penjualan/pembelian) ke CSV.
    """
    transaksi_list = load_csv(DATA_TRANSAKSI_FILE)

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Kode Transaksi",
            "Tanggal",
            "Jenis",
            "Kode Barang",
            "Jumlah"
        ])

        for trx in transaksi_list:
            if trx["jenis"] == jenis:
                writer.writerow([
                    trx["kode_transaksi"],
                    trx["tanggal"],
                    trx["jenis"],
                    trx["kode_barang"],
                    trx["jumlah"]
                ])

def export_transaksi_to_pdf(jenis, filename, judul):
    """
    Mengekspor laporan transaksi (penjualan/pembelian) ke PDF.
    """
    transaksi_list = load_csv(DATA_TRANSAKSI_FILE)
    pdf = canvas.Canvas(filename, pagesize=A4)

    width, height = A4
    y = height - 50

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, judul)
    y -= 30

    pdf.setFont("Helvetica", 10)

    # Header
    pdf.drawString(50, y, "Kode")
    pdf.drawString(120, y, "Tanggal")
    pdf.drawString(220, y, "Barang")
    pdf.drawString(300, y, "Jumlah")
    y -= 20

    for trx in transaksi_list:
        if trx["jenis"] == jenis:
            pdf.drawString(50, y, trx["kode_transaksi"])
            pdf.drawString(120, y, trx["tanggal"])
            pdf.drawString(220, y, trx["kode_barang"])
            pdf.drawString(300, y, trx["jumlah"])
            y -= 18

            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - 50

    pdf.save()

