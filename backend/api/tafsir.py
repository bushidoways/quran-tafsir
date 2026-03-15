"""
Tafsir Router

Router utama untuk endpoint tafsir Al-Qur'an.
"""
from fastapi import APIRouter, Query, Path

router = APIRouter(tags=["Tafsir"])


@router.get("/search")
async def search_tafsir(
    q: str = Query(..., description="Kata kunci pencarian"),
    mufassir: str = Query("ibn-kathir", description="ID mufassir"),
):
    """Cari tafsir berdasarkan kata kunci."""
    return {
        "query": q,
        "mufassir": mufassir,
        "results": [],
    }


@router.get("/tafsir/{surah}/{ayah}")
async def get_tafsir(
    surah: int = Path(..., ge=1, le=114),
    ayah: int = Path(..., ge=1),
    mufassir: str = Query("ibn-kathir"),
):
    """Ambil tafsir untuk surah dan ayat tertentu."""

    # Contoh response untuk testing
    if surah == 1 and ayah == 1:
        return {
            "surah": 1,
            "ayah": 1,
            "text_arab": "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
            "terjemahan": "Dengan nama Allah Yang Maha Pengasih, Maha Penyayang.",
            "tafsir": (
                "Bismillah adalah pembuka segala urusan. Para ulama terdahulu memulai "
                "setiap perkara penting dengan bismillah. Nama 'Allah' adalah nama Dzat "
                "yang disembah, sedangkan Ar-Rahman dan Ar-Rahim adalah dua nama yang "
                "menunjukkan betapa luasnya kasih sayang Allah."
            ),
            "mufassir": mufassir,
            "quote": "Sesungguhnya Al-Qur'an ini memberi petunjuk ke jalan yang paling lurus. (QS. Al-Isra: 9)",
        }

    return {
        "surah": surah,
        "ayah": ayah,
        "mufassir": mufassir,
        "tafsir": "Tafsir akan dimuat dari sumber terverifikasi.",
    }
