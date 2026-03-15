"""
Layanan Tematik

Service untuk mengelola dan mencari koneksi tematik antar ayat Al-Qur'an.
"""
from typing import Dict, Any, List

THEMATIC_CONNECTIONS = {
    "sabar": {
        "label": "Sabar dan Ketabahan",
        "ayat": [
            {"surah": 2, "ayah": 153, "ringkasan": "Minta tolong dengan sabar dan shalat"},
            {"surah": 2, "ayah": 286, "ringkasan": "Allah tidak membebani di luar kemampuan"},
            {"surah": 3, "ayah": 200, "ringkasan": "Bersabarlah dan kuatkan kesabaranmu"},
            {"surah": 94, "ayah": 6, "ringkasan": "Bersama kesulitan ada kemudahan"},
        ],
    },
    "tawakkal": {
        "label": "Tawakkal kepada Allah",
        "ayat": [
            {"surah": 65, "ayah": 3, "ringkasan": "Barangsiapa bertawakkal, Allah mencukupinya"},
            {"surah": 3, "ayah": 159, "ringkasan": "Bertawakkallah kepada Allah"},
            {"surah": 8, "ayah": 2, "ringkasan": "Kepada Allah mereka bertawakkal"},
        ],
    },
    "ilmu": {
        "label": "Ilmu dan Pengetahuan",
        "ayat": [
            {"surah": 96, "ayah": 1, "ringkasan": "Bacalah dengan nama Tuhanmu"},
            {"surah": 20, "ayah": 114, "ringkasan": "Ya Tuhanku, tambahkanlah ilmuku"},
            {"surah": 58, "ayah": 11, "ringkasan": "Allah meninggikan derajat orang berilmu"},
        ],
    },
    "doa": {
        "label": "Doa dan Munajat",
        "ayat": [
            {"surah": 2, "ayah": 186, "ringkasan": "Sesungguhnya Aku dekat"},
            {"surah": 40, "ayah": 60, "ringkasan": "Berdoalah kepada-Ku"},
            {"surah": 7, "ayah": 55, "ringkasan": "Berdoalah dengan rendah hati"},
        ],
    },
    "tauhid": {
        "label": "Tauhid dan Keimanan",
        "ayat": [
            {"surah": 112, "ayah": 1, "ringkasan": "Katakanlah: Allah itu Esa"},
            {"surah": 2, "ayah": 255, "ringkasan": "Ayat Kursi - Allah, tidak ada ilah selain Dia"},
            {"surah": 3, "ayah": 18, "ringkasan": "Allah menyaksikan bahwa tiada ilah selain Dia"},
        ],
    },
}


class ThematicService:
    """Service untuk pencarian dan koneksi tematik Al-Qur'an."""

    def get_connections(self, theme: str) -> Dict[str, Any]:
        """Ambil koneksi tematik berdasarkan tema."""
        if theme.lower() in THEMATIC_CONNECTIONS:
            data = THEMATIC_CONNECTIONS[theme.lower()]
            return {
                "theme": theme,
                "label": data["label"],
                "total_ayat": len(data["ayat"]),
                "ayat": data["ayat"],
            }
        return {"theme": theme, "error": "Tema tidak ditemukan dalam database"}

    def list_themes(self) -> List[Dict[str, Any]]:
        """Tampilkan semua tema yang tersedia."""
        return [
            {"id": k, "label": v["label"], "total_ayat": len(v["ayat"])}
            for k, v in THEMATIC_CONNECTIONS.items()
        ]
