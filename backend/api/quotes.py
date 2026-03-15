"""
Quotes Router

Endpoint untuk quotes dan ayat-ayat pilihan Al-Qur'an.
"""
from fastapi import APIRouter

router = APIRouter(tags=["Quotes"])


@router.get("/quotes/random")
async def get_random_quote():
    """Ambil quotes Al-Qur'an secara acak."""
    return {
        "text": "Sesungguhnya bersama kesulitan ada kemudahan.",
        "surah": "Al-Insyirah",
        "ayah": 6,
        "theme": "sabar",
    }


@router.get("/quotes/daily")
async def get_daily_quote():
    """Ambil ayat harian untuk inspirasi."""
    return {
        "text": "Dan apabila hamba-hamba-Ku bertanya kepadamu tentang Aku, maka sesungguhnya Aku dekat.",
        "surah": "Al-Baqarah",
        "ayah": 186,
        "theme": "doa",
    }
