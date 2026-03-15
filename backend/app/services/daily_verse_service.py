"""
Layanan Ayat Harian

Service untuk menampilkan ayat harian beserta tafsir ringkasnya.
"""
import random
from datetime import date
from typing import Dict, Any

DAILY_VERSES = [
    {"surah": 2, "ayah": 286, "theme": "sabar"},
    {"surah": 3, "ayah": 139, "theme": "semangat"},
    {"surah": 94, "ayah": 6, "theme": "harapan"},
    {"surah": 2, "ayah": 152, "theme": "dzikir"},
    {"surah": 65, "ayah": 3, "theme": "tawakkal"},
    {"surah": 40, "ayah": 60, "theme": "doa"},
    {"surah": 17, "ayah": 9, "theme": "hidayah"},
    {"surah": 13, "ayah": 11, "theme": "ikhtiar"},
    {"surah": 2, "ayah": 186, "theme": "doa"},
    {"surah": 17, "ayah": 82, "theme": "syifa"},
]


class DailyVerseService:
    """Service untuk menyediakan ayat harian."""

    def get_daily_verse(self) -> Dict[str, Any]:
        """
        Ambil ayat harian berdasarkan tanggal.
        Menggunakan tanggal sebagai seed agar konsisten dalam satu hari.
        """
        today = date.today()
        seed = today.year * 10000 + today.month * 100 + today.day
        random.seed(seed)
        verse = random.choice(DAILY_VERSES)
        random.seed()  # Reset seed

        return {
            "surah": verse["surah"],
            "ayah": verse["ayah"],
            "theme": verse["theme"],
            "date": str(today),
        }
