"""
Layanan Quran

Service untuk mengambil data Al-Qur'an (ayat, surah, terjemahan).
"""
import httpx
from typing import Dict, Any, List, Optional
from backend.app.core.config import settings


class QuranService:
    """Service untuk mengambil data Al-Qur'an dari berbagai API."""

    def __init__(self):
        self.quran_api = settings.QURAN_API_BASE
        self.alquran_cloud = settings.ALQURAN_CLOUD_API

    async def get_ayah(self, surah: int, ayah: int) -> Dict[str, Any]:
        """Ambil teks ayat beserta terjemahannya."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.alquran_cloud}/ayah/{surah}:{ayah}/editions/quran-uthmani,id.indonesian"
                )
                if response.status_code == 200:
                    data = response.json()
                    editions = data.get("data", [])
                    return {
                        "surah": surah,
                        "ayah": ayah,
                        "text_arab": editions[0]["text"] if len(editions) > 0 else "",
                        "terjemahan": editions[1]["text"] if len(editions) > 1 else "",
                    }
        except Exception as e:
            return {"error": f"Gagal mengambil data ayat: {str(e)}"}

        return {"error": "Data ayat tidak tersedia"}

    async def get_surah_info(self, surah_number: int) -> Dict[str, Any]:
        """Ambil informasi detail surah."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.alquran_cloud}/surah/{surah_number}"
                )
                if response.status_code == 200:
                    data = response.json().get("data", {})
                    return {
                        "number": data.get("number"),
                        "name": data.get("englishName"),
                        "name_arab": data.get("name"),
                        "total_ayah": data.get("numberOfAyahs"),
                        "tempat_turun": data.get("revelationType"),
                    }
        except Exception as e:
            return {"error": f"Gagal mengambil info surah: {str(e)}"}

        return {"error": "Info surah tidak tersedia"}
