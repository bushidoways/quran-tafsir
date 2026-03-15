"""
Fitur API Routes

Endpoint untuk menampilkan fitur-fitur yang tersedia di platform.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/features",
    summary="Daftar fitur platform",
    description="Menampilkan semua fitur yang tersedia di platform Quran Tafsir",
    tags=["Fitur"],
)
async def list_features():
    """Tampilkan daftar fitur yang tersedia."""
    return {
        "features": [
            {
                "name": "Pencarian Tafsir",
                "description": "Cari tafsir berdasarkan kata kunci, surah, atau ayat tertentu",
                "status": "aktif",
            },
            {
                "name": "Multi-Tafsir",
                "description": "Bandingkan tafsir dari berbagai mufassir terpercaya secara berdampingan",
                "status": "aktif",
            },
            {
                "name": "Quotes Harian",
                "description": "Dapatkan ayat Al-Qur'an pilihan setiap hari untuk inspirasi",
                "status": "aktif",
            },
            {
                "name": "Koneksi Tematik",
                "description": "Temukan ayat-ayat yang saling berkaitan secara tema dan konteks",
                "status": "aktif",
            },
            {
                "name": "Analitik Tematik",
                "description": "Statistik distribusi tema dan topik dalam Al-Qur'an",
                "status": "aktif",
            },
            {
                "name": "Asisten AI",
                "description": "Tanya jawab seputar tafsir dengan bantuan kecerdasan buatan",
                "status": "beta",
            },
            {
                "name": "Audio Murattal",
                "description": "Dengarkan bacaan Al-Qur'an dari qari pilihan",
                "status": "segera hadir",
            },
            {
                "name": "Catatan Studi",
                "description": "Simpan catatan pribadi dan bookmark untuk ayat-ayat tertentu",
                "status": "segera hadir",
            },
        ]
    }
