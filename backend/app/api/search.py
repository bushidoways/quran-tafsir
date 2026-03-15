"""
Pencarian API Routes

Endpoint untuk pencarian ayat, tafsir, dan konten Al-Qur'an.
"""
from fastapi import APIRouter, Query

router = APIRouter()


@router.get(
    "/search",
    summary="Cari ayat dan tafsir",
    description="Pencarian teks lengkap di seluruh database tafsir",
    tags=["Pencarian"],
)
async def search(
    q: str = Query(..., description="Kata kunci pencarian"),
    mufassir: str = Query("ibn-kathir", description="ID mufassir"),
    page: int = Query(1, ge=1, description="Nomor halaman"),
    limit: int = Query(10, ge=1, le=50, description="Jumlah hasil per halaman"),
):
    """
    Cari ayat dan tafsir berdasarkan kata kunci.

    Mendukung pencarian dalam:
    - Teks ayat (terjemahan Indonesia)
    - Konten tafsir
    - Nama surah
    """
    return {
        "query": q,
        "mufassir": mufassir,
        "page": page,
        "limit": limit,
        "total_results": 0,
        "results": [],
    }
