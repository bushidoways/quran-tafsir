"""
Tafsir API Routes

Endpoint untuk mengakses tafsir Al-Qur'an dari berbagai mufassir terverifikasi.
"""
from fastapi import APIRouter, Path, Query
from backend.app.data.mufassireen import MUFASSIREEN
from backend.app.services.tafsir_service import TafsirService

router = APIRouter()
tafsir_service = TafsirService()


@router.get(
    "/mufassireen",
    summary="Daftar mufassir",
    description="Menampilkan semua mufassir (penulis tafsir) yang telah diverifikasi",
    tags=["Tafsir"],
)
async def list_mufassireen():
    """Tampilkan daftar mufassir yang tersedia."""
    return {
        "total": len(MUFASSIREEN),
        "mufassireen": [
            {
                "id": m["id"],
                "name": m["name"],
                "kitab": m["kitab"],
                "era": m["era"],
            }
            for m in MUFASSIREEN
        ],
    }


@router.get(
    "/tafsir/{surah}/{ayah}",
    summary="Ambil tafsir ayat",
    description="Menampilkan tafsir untuk ayat tertentu dari mufassir pilihan",
    tags=["Tafsir"],
)
async def get_tafsir(
    surah: int = Path(..., ge=1, le=114, description="Nomor surah"),
    ayah: int = Path(..., ge=1, description="Nomor ayat"),
    mufassir: str = Query("ibn-kathir", description="ID mufassir"),
):
    """Ambil tafsir untuk surah dan ayat tertentu."""
    result = await tafsir_service.get_tafsir(surah, ayah, mufassir)
    return result
