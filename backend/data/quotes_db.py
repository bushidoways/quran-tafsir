"""
Database Quotes

Kumpulan quotes Al-Qur'an yang dikategorikan berdasarkan tema.
"""
import random
from typing import Dict, Any, List, Optional

QUOTES_DATABASE = [
    {
        "id": 1,
        "text": "Sesungguhnya bersama kesulitan ada kemudahan.",
        "surah_name": "Al-Insyirah",
        "surah_number": 94,
        "ayah": 6,
        "theme": "sabar",
    },
    {
        "id": 2,
        "text": "Dan apabila hamba-hamba-Ku bertanya kepadamu tentang Aku, maka sesungguhnya Aku dekat.",
        "surah_name": "Al-Baqarah",
        "surah_number": 2,
        "ayah": 186,
        "theme": "doa",
    },
    {
        "id": 3,
        "text": "Barangsiapa bertakwa kepada Allah, niscaya Dia akan membukakan jalan keluar baginya.",
        "surah_name": "At-Talaq",
        "surah_number": 65,
        "ayah": 2,
        "theme": "tawakkal",
    },
    {
        "id": 4,
        "text": "Maka ingatlah kepada-Ku, niscaya Aku akan mengingat kalian.",
        "surah_name": "Al-Baqarah",
        "surah_number": 2,
        "ayah": 152,
        "theme": "dzikir",
    },
    {
        "id": 5,
        "text": "Allah tidak membebani seseorang melainkan sesuai dengan kesanggupannya.",
        "surah_name": "Al-Baqarah",
        "surah_number": 2,
        "ayah": 286,
        "theme": "sabar",
    },
]


def get_random_quote() -> Dict[str, Any]:
    """Ambil satu quotes acak."""
    return random.choice(QUOTES_DATABASE)


def get_quotes_by_theme(theme: str) -> List[Dict[str, Any]]:
    """Ambil quotes berdasarkan tema."""
    return [q for q in QUOTES_DATABASE if q["theme"] == theme]


def get_all_themes() -> List[str]:
    """Tampilkan semua tema yang tersedia."""
    return list(set(q["theme"] for q in QUOTES_DATABASE))
