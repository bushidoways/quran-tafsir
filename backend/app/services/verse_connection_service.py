"""
Layanan Koneksi Ayat

Service untuk menemukan hubungan dan keterkaitan antar ayat Al-Qur'an.
"""
from typing import Dict, Any, List


class VerseConnectionService:
    """Service untuk menemukan koneksi antar ayat Al-Qur'an."""

    # Contoh mapping koneksi ayat
    CONNECTIONS = {
        "2:255": ["3:2", "59:23", "112:1"],  # Ayat tentang keesaan Allah
        "2:286": ["7:42", "23:62", "65:7"],  # Ayat tentang kemudahan
        "2:152": ["29:45", "33:41", "73:8"],  # Ayat tentang dzikir
    }

    def find_connections(self, surah: int, ayah: int) -> Dict[str, Any]:
        """
        Cari ayat-ayat yang berkaitan dengan ayat tertentu.

        Parameter:
            surah: Nomor surah
            ayah: Nomor ayat

        Return:
            Dictionary berisi daftar ayat yang saling terkait
        """
        key = f"{surah}:{ayah}"
        connections = self.CONNECTIONS.get(key, [])

        return {
            "source": {"surah": surah, "ayah": ayah},
            "connections": [
                {
                    "reference": ref,
                    "surah": int(ref.split(":")[0]),
                    "ayah": int(ref.split(":")[1]),
                }
                for ref in connections
            ],
            "total": len(connections),
        }
