"""
Modul ini bertanggung jawab untuk membaca dan menyimpan
data ke file CSV. Tidak mengandung logic bisnis apa pun.
"""

import csv
import os

def load_csv(filepath):
    """
    Membaca file CSV dan mengembalikan data dalam bentuk list of dictionary.
    Jika file tidak ditemukan, akan mengembalikan list kosong.
    """
    data = []

    try:
        # Cek apakah file ada
        if not os.path.exists(filepath):
            return data

        # Membaca file CSV
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

    except Exception as e:
        # Error handling jika terjadi masalah saat membaca file
        raise RuntimeError(f"Gagal membaca file {filepath}: {e}")

    return data


def save_csv(filepath, fieldnames, data):
    """
    Menyimpan list of dictionary ke file CSV.
    """
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    except Exception as e:
        # Error handling saat menyimpan file
        raise RuntimeError(f"Gagal menyimpan file {filepath}: {e}")
