"""
Surah API Routes

Endpoint untuk data surah Al-Qur'an.
"""
from fastapi import APIRouter, Path
from backend.app.data.surah_index import SURAH_INDEX

router = APIRouter()


@router.get(
    "/surah",
    summary="Daftar semua surah",
    description="Menampilkan daftar lengkap 114 surah dalam Al-Qur'an",
    tags=["Surah"],
)
async def list_surahs():
    """Tampilkan daftar seluruh surah Al-Qur'an."""
    return {"total": 114, "surahs": SURAH_INDEX}


@router.get(
    "/surah/{surah_number}",
    summary="Detail surah tertentu",
    description="Menampilkan informasi lengkap surah berdasarkan nomor",
    tags=["Surah"],
)
async def get_surah(surah_number: int = Path(..., ge=1, le=114)):
    """Ambil detail surah berdasarkan nomor (1-114)."""
    for s in SURAH_INDEX:
        if s["number"] == surah_number:
            return s
    return {"error": "Surah tidak ditemukan"}
