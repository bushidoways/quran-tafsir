"""
Validator Sumber Tafsir

Modul untuk memvalidasi apakah sumber tafsir berasal dari ulama yang terverifikasi.
"""
from typing import Tuple

VERIFIED_SOURCES = {
    "ibn-kathir": {
        "full_name": "Ibnu Katsir",
        "kitab": "Tafsir Al-Qur'an Al-'Azhim",
        "verification_level": "TERVERIFIKASI"
    },
    "as-sadi": {
        "full_name": "As-Sa'di",
        "kitab": "Taisir Al-Karim Ar-Rahman",
        "verification_level": "TERVERIFIKASI"
    },
    "al-tabari": {
        "full_name": "At-Tabari",
        "kitab": "Jami' Al-Bayan",
        "verification_level": "TERVERIFIKASI"
    },
    "al-baghawi": {
        "full_name": "Al-Baghawi",
        "kitab": "Ma'alim At-Tanzil",
        "verification_level": "TERVERIFIKASI"
    },
}


def validate_mufassir(mufassir_id: str) -> Tuple[bool, str]:
    """
    Validasi apakah mufassir termasuk dalam daftar ulama yang diakui.

    Parameter:
        mufassir_id: ID unik mufassir

    Return:
        Tuple (status_valid, pesan)
    """
    info = VERIFIED_SOURCES.get(mufassir_id)
    if info:
        return True, f"Terverifikasi: {info['full_name']} -- {info['kitab']}"
    if mufassir_id in ["ibn-rajab", "as-shanqiti", "ibn-abi-hatim", "ibn-al-qayyim", "ibn-abbas", "al-uthaymeen"]:
        return True, f"Terverifikasi: {mufassir_id} termasuk ulama yang diakui"
    return False, f"Tidak dikenal: {mufassir_id} belum ada dalam database verifikasi"
