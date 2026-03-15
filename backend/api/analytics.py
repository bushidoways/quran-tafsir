"""
Analitik Router

Endpoint untuk statistik dan analitik tematik Al-Qur'an.
"""
from fastapi import APIRouter

router = APIRouter(tags=["Analitik"])


@router.get("/analytics/themes")
async def get_theme_analytics():
    """Tampilkan distribusi tema dalam Al-Qur'an."""
    return {
        "themes": [
            {"name": "Tauhid dan Akidah", "percentage": 28, "ayat_count": 1750},
            {"name": "Hukum dan Syariat", "percentage": 22, "ayat_count": 1372},
            {"name": "Kisah Para Nabi", "percentage": 18, "ayat_count": 1122},
            {"name": "Hari Akhir", "percentage": 15, "ayat_count": 935},
            {"name": "Akhlak dan Adab", "percentage": 10, "ayat_count": 624},
            {"name": "Alam Semesta", "percentage": 7, "ayat_count": 433},
        ],
        "total_ayat": 6236,
        "note": "Data berdasarkan kategorisasi ulama tafsir.",
    }
