"""
Quran Tafsir - Aplikasi Utama

File utama untuk konfigurasi dan inisialisasi FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api import features, search, surah, tafsir

def create_app() -> FastAPI:
    """Buat dan konfigurasi aplikasi FastAPI."""

    print("=" * 50)
    print("Platform Tafsir Al-Qur'an")
    print(f"Versi: {settings.APP_VERSION}")
    print("=" * 50)

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "**Platform Pencarian Tafsir Al-Qur'an Terverifikasi.**\n\n"
            "Fitur utama:\n"
            "- Pencarian ayat dan tafsir\n"
            "- Multi-tafsir dari ulama terpercaya (Ibn Kathir, At-Tabari, As-Sa'di, dll)\n"
            "- Perbandingan tafsir berdampingan\n"
            "- Quotes Al-Qur'an relevan di setiap pencarian\n"
            "- Ayat harian dengan tafsir ringkas\n"
            "- Koneksi tematik antar ayat\n"
            "- Audio murattal\n"
            "- Catatan studi dan bookmark\n"
            "- Tracking progress belajar\n"
            "- Indeks tematik Al-Qur'an\n\n"
            "Semua sumber tafsir telah diverifikasi dan divalidasi."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Daftarkan router
    app.include_router(features.router, prefix="/api/v1", tags=["Fitur"])
    app.include_router(search.router, prefix="/api/v1", tags=["Pencarian"])
    app.include_router(surah.router, prefix="/api/v1", tags=["Surah"])
    app.include_router(tafsir.router, prefix="/api/v1", tags=["Tafsir"])

    return app

app = create_app()
