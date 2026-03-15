"""
Konfigurasi Aplikasi

Pengaturan utama untuk seluruh aplikasi, termasuk koneksi API dan variabel lingkungan.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Konfigurasi utama aplikasi."""

    APP_NAME: str = "Quran Tafsir"
    APP_VERSION: str = "2.0.0"
    APP_DESCRIPTION: str = (
        "Platform pencarian tafsir Al-Qur'an yang terverifikasi dan tervalidasi"
    )

    # API Keys (opsional)
    QURAN_API_BASE: str = "https://api.quran.com/api/v4"
    TAFSIR_API_BASE: str = "https://api.quran-tafseer.com"
    ALQURAN_CLOUD_API: str = "https://api.alquran.cloud/v1"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
