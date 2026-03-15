"""
Asisten AI Router

Tanya jawab berbasis konteks tafsir menggunakan RAG (Retrieval-Augmented Generation).
"""
from fastapi import APIRouter, Query

router = APIRouter(tags=["Asisten AI"])


@router.get("/ai/ask")
async def ask_ai(
    question: str = Query(..., description="Pertanyaan seputar tafsir Al-Qur'an"),
):
    """
    Ajukan pertanyaan tentang ayat atau tafsir Al-Qur'an.
    Jawaban dihasilkan berdasarkan konteks dari ulama terpercaya.

    Catatan: Fitur ini dalam tahap beta. Jawaban akan selalu merujuk
    pada sumber tafsir yang terverifikasi.
    """

    # Contoh response (nanti akan dihubungkan ke model AI)
    return {
        "question": question,
        "answer": (
            "Pertanyaan Anda sedang diproses. Fitur asisten AI masih dalam "
            "tahap pengembangan. Jawaban akan selalu merujuk pada tafsir dari "
            "ulama yang diakui oleh Ahlus Sunnah wal Jama'ah."
        ),
        "sources": [
            {"mufassir": "Ibn Kathir", "kitab": "Tafsir Al-Qur'an Al-'Azhim"},
        ],
        "disclaimer": "Jawaban ini berbasis konteks tafsir ulama. Wallahu A'lam bish-shawab.",
    }


@router.get("/ai/validate")
async def validate_source(
    mufassir_id: str = Query(..., description="ID mufassir yang akan divalidasi"),
):
    """
    Validasi apakah sumber tafsir sesuai standar Ahlus Sunnah.
    """
    verified_mufassir = [
        "ibn-kathir", "as-sadi", "al-tabari", "al-baghawi",
        "ibn-rajab", "as-shanqiti", "ibn-abi-hatim",
        "ibn-al-qayyim", "ibn-abbas", "al-uthaymeen",
    ]

    if mufassir_id in verified_mufassir:
        return {
            "mufassir_id": mufassir_id,
            "status": "terverifikasi",
            "message": f"Mufassir '{mufassir_id}' termasuk dalam daftar ulama terverifikasi.",
        }
    else:
        return {
            "mufassir_id": mufassir_id,
            "status": "tidak dikenal",
            "message": f"Mufassir '{mufassir_id}' belum ada dalam database verifikasi.",
        }
