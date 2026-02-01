"""
Modul ini berisi fungsi validasi data 
untuk mencegah input tidak valid.
"""

def validate_not_empty(value, field_name):
    """
    Memastikan sebuah field tidak kosong.
    """
    if not value:
        raise ValueError(f"{field_name} tidak boleh kosong")


def validate_positive_number(value, field_name):
    """
    Memastikan sebuah nilai numerik tidak negatif.
    """
    if value < 0:
        raise ValueError(f"{field_name} tidak boleh bernilai negatif")
