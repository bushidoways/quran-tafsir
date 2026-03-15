"""
Layanan Tafsir

Service utama untuk mengambil tafsir dari berbagai sumber API terverifikasi.
"""
import httpx
from typing import Optional, Dict, Any
from backend.app.core.config import settings
from backend.app.data.mufassireen import MUFASSIREEN


class TafsirService:
    """Service untuk mengambil tafsir dari sumber yang terverifikasi."""

    def __init__(self):
        self.quran_api = settings.QURAN_API_BASE
        self.tafsir_api = settings.TAFSIR_API_BASE
        self.alquran_cloud = settings.ALQURAN_CLOUD_API

    async def get_tafsir(
        self, surah: int, ayah: int, mufassir_id: str = "ibn-kathir"
    ) -> Dict[str, Any]:
        """
        Ambil tafsir untuk ayat tertentu dari mufassir yang dipilih.

        Parameter:
            surah: Nomor surah (1-114)
            ayah: Nomor ayat
            mufassir_id: ID mufassir (default: ibn-kathir)

        Return:
            Dictionary berisi data tafsir lengkap
        """
        mufassir = self._get_mufassir(mufassir_id)
        if not mufassir:
            return {"error": f"Mufassir '{mufassir_id}' tidak ditemukan dalam database"}

        tafsir_data = await self._fetch_from_api(surah, ayah, mufassir)

        return {
            "surah": surah,
            "ayah": ayah,
            "mufassir": {
                "id": mufassir["id"],
                "name": mufassir["name"],
                "kitab": mufassir["kitab"],
            },
            "tafsir": tafsir_data,
        }

    def _get_mufassir(self, mufassir_id: str) -> Optional[Dict]:
        """Cari data mufassir berdasarkan ID."""
        for m in MUFASSIREEN:
            if m["id"] == mufassir_id:
                return m
        return None

    async def _fetch_from_api(
        self, surah: int, ayah: int, mufassir: Dict
    ) -> Dict[str, Any]:
        """Ambil data tafsir dari API eksternal."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if mufassir.get("api_id"):
                    response = await client.get(
                        f"{self.tafsir_api}/tafseer/{mufassir['api_id']}/{surah}/{ayah}"
                    )
                    if response.status_code == 200:
                        data = response.json()
                        return {
                            "text": data.get("text", ""),
                            "source": mufassir["kitab"],
                            "source_api": "quran-tafseer.com",
                        }

                # Fallback ke AlQuran Cloud API
                response = await client.get(
                    f"{self.alquran_cloud}/ayah/{surah}:{ayah}/editions/quran-uthmani,id.indonesian"
                )
                if response.status_code == 200:
                    data = response.json()
                    editions = data.get("data", [])
                    return {
                        "text_arab": editions[0]["text"] if len(editions) > 0 else "",
                        "terjemahan": editions[1]["text"] if len(editions) > 1 else "",
                        "source": "AlQuran Cloud API",
                        "note": f"Tafsir {mufassir['kitab']} belum tersedia via API. Ditampilkan terjemahan sebagai gantinya.",
                    }

        except Exception as e:
            return {
                "error": f"Gagal mengambil tafsir: {str(e)}",
                "fallback": True,
            }

        return {"error": "Data tafsir tidak tersedia untuk ayat ini"}
