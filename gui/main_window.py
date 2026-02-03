"""
Modul antarmuka pengguna (GUI) menggunakan Tkinter.
GUI berfungsi sebagai layer presentasi.
Seluruh logika bisnis ditangani oleh service dan class.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from datetime import date

from services.transaksi_service import transaksi_pembelian, transaksi_penjualan
from services.laporan_service import get_stok_akhir
from services.export_service import (
    export_stok_to_csv,
    export_stok_to_pdf,
    export_transaksi_to_csv,
    export_transaksi_to_pdf
)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Manajemen UMKM")

        self.create_table()
        self.create_refresh()
        self.create_form_transaksi()
        self.create_export_section()

        self.load_barang()

    # ================= TABLE =================
    def create_table(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            frame,
            columns=("kode", "nama", "stok"),
            show="headings"
        )
        self.tree.heading("kode", text="Kode")
        self.tree.heading("nama", text="Nama Barang")
        self.tree.heading("stok", text="Stok")
        self.tree.pack(fill=tk.BOTH, expand=True)

    # ================= REFRESH =================
    def create_refresh(self):
        tk.Button(
            self.root,
            text="Refresh Data",
            width=20,
            command=self.load_barang
        ).pack(pady=5)

    # ================= FORM TRANSAKSI =================
    def create_form_transaksi(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Tanggal (YYYY-MM-DD)").grid(row=0, column=0, padx=5)
        tk.Label(frame, text="Kode Barang").grid(row=0, column=1, padx=5)
        tk.Label(frame, text="Jumlah").grid(row=0, column=2, padx=5)

        self.ent_tanggal = tk.Entry(frame, width=15, state="readonly")
        self.ent_tanggal.grid(row=1, column=0, padx=5)

        # set default hari ini
        self.ent_tanggal.config(state="normal")
        self.ent_tanggal.insert(0, date.today().strftime("%Y-%m-%d"))
        self.ent_tanggal.config(state="readonly")

        # klik untuk buka kalender
        self.ent_tanggal.bind("<Button-1>", self.open_calendar)

        self.ent_kode_barang = tk.Entry(frame, width=15)
        self.ent_jumlah = tk.Entry(frame, width=10)

        self.ent_tanggal.grid(row=1, column=0, padx=5)
        self.ent_kode_barang.grid(row=1, column=1, padx=5)
        self.ent_jumlah.grid(row=1, column=2, padx=5)

        frame_btn = tk.Frame(frame)
        frame_btn.grid(row=2, column=0, columnspan=3, pady=10)

        tk.Button(
            frame_btn,
            text="Pembelian",
            width=15,
            command=self.handle_pembelian
        ).grid(row=0, column=0, padx=20)

        tk.Button(
            frame_btn,
            text="Penjualan",
            width=15,
            command=self.handle_penjualan
        ).grid(row=0, column=1, padx=20)
    
    def open_calendar(self, event=None):
        cal_win = tk.Toplevel(self.root)
        cal_win.title("Pilih Tanggal")
        cal_win.resizable(False, False)

        cal = Calendar(
            cal_win,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            maxdate=date.today()   # ⬅️ BLOK FUTURE DATE
        )
        cal.pack(padx=10, pady=10)

        def pilih_tanggal():
            selected = cal.get_date()
            self.ent_tanggal.config(state="normal")
            self.ent_tanggal.delete(0, tk.END)
            self.ent_tanggal.insert(0, selected)
            self.ent_tanggal.config(state="readonly")
            cal_win.destroy()

        tk.Button(
            cal_win,
            text="Pilih",
            command=pilih_tanggal
        ).pack(pady=5)


    # ================= EXPORT =================
    def create_export_section(self):
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=15)

        # Export stok
        tk.Button(
            self.root,
            text="Export Laporan Stok",
            width=30,
            command=self.handle_export_stok
        ).pack(pady=5)

        # Export transaksi
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(
            frame,
            text="Export Laporan Penjualan",
            width=25,
            command=self.handle_export_penjualan
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            frame,
            text="Export Laporan Pembelian",
            width=25,
            command=self.handle_export_pembelian
        ).grid(row=0, column=1, padx=10)

    # ================= DATA =================
    def load_barang(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for barang in get_stok_akhir():
            self.tree.insert(
                "",
                tk.END,
                values=(barang["kode"], barang["nama"], barang["stok"])
            )

    # ================= HANDLER =================
    def handle_pembelian(self):
        try:
            tanggal = self.ent_tanggal.get()
            kode_barang = self.ent_kode_barang.get()
            jumlah_text = self.ent_jumlah.get().strip()

            # Validasi input kosong
            if not tanggal or not kode_barang or not jumlah_text:
                messagebox.showerror("Error", "Semua field harus diisi")
                return

            # Validasi numerik
            if not jumlah_text.isdigit():
                messagebox.showerror("Error", "Jumlah harus berupa angka")
                return

            jumlah = int(jumlah_text)

            transaksi_pembelian(tanggal, kode_barang, jumlah)
            messagebox.showinfo("Sukses", "Pembelian berhasil")
            self.load_barang()
            self.ent_kode_barang.delete(0, tk.END)
            self.ent_jumlah.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_penjualan(self):
        try:
            tanggal = self.ent_tanggal.get()
            kode_barang = self.ent_kode_barang.get()
            jumlah_text = self.ent_jumlah.get().strip()

            if not tanggal or not kode_barang or not jumlah_text:
                messagebox.showerror("Error", "Semua field harus diisi")
                return

            if not jumlah_text.isdigit():
                messagebox.showerror("Error", "Jumlah harus berupa angka")
                return

            jumlah = int(jumlah_text)

            transaksi_penjualan(tanggal, kode_barang, jumlah)
            messagebox.showinfo("Sukses", "Penjualan berhasil")
            self.load_barang()
            self.ent_kode_barang.delete(0, tk.END)
            self.ent_jumlah.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= EXPORT HANDLER =================
    def handle_export_stok(self):
        self._export_dialog(
            export_stok_to_csv,
            export_stok_to_pdf,
            "Laporan stok berhasil diekspor"
        )

    def handle_export_penjualan(self):
        self._export_dialog(
            lambda: export_transaksi_to_csv("penjualan", "laporan_penjualan.csv"),
            lambda: export_transaksi_to_pdf("penjualan", "laporan_penjualan.pdf", "Laporan Penjualan"),
            "Laporan penjualan berhasil diekspor"
        )

    def handle_export_pembelian(self):
        self._export_dialog(
            lambda: export_transaksi_to_csv("pembelian", "laporan_pembelian.csv"),
            lambda: export_transaksi_to_pdf("pembelian", "laporan_pembelian.pdf", "Laporan Pembelian"),
            "Laporan pembelian berhasil diekspor"
        )

    def _export_dialog(self, csv_func, pdf_func, success_msg):
        dialog = tk.Toplevel(self.root)
        dialog.title("Export Laporan")
        dialog.geometry("300x120")
        dialog.resizable(False, False)

        tk.Label(dialog, text="Pilih format export:", pady=10).pack()

        frame = tk.Frame(dialog)
        frame.pack(pady=10)

        tk.Button(
            frame,
            text="CSV",
            width=12,
            command=lambda: (csv_func(), messagebox.showinfo("Sukses", success_msg), dialog.destroy())
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            frame,
            text="PDF",
            width=12,
            command=lambda: (pdf_func(), messagebox.showinfo("Sukses", success_msg), dialog.destroy())
        ).grid(row=0, column=1, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
