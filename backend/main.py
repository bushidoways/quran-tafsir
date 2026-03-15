"""
Quran Tafsir - Backend API

Server utama untuk menjalankan semua endpoint API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- Import Router ---
from backend.api.tafsir import router as tafsir_router
from backend.api.quotes import router as quotes_router
from backend.api.analytics import router as analytics_router
from backend.api.ai_assistant import router as ai_router

# --- Inisialisasi Aplikasi ---
app = FastAPI(
    title="Quran Tafsir API",
    description="API untuk pencarian tafsir Al-Qur'an yang terverifikasi dan tervalidasi",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Daftarkan Router ---
app.include_router(tafsir_router, prefix="/api/v1")
app.include_router(quotes_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")


# --- Endpoints Utama ---
# --- Pencarian Tafsir ---
@app.get("/api/v1/search", tags=["Pencarian"])
async def search_tafsir(q: str, mufassir: str = "ibn-kathir"):
    """
    Cari tafsir berdasarkan kata kunci.

    Parameter:
    - q: Kata kunci pencarian (contoh: "sabar", "taubat", "rezeki")
    - mufassir: ID mufassir yang dipilih (default: ibn-kathir)
    """
    return {
        "query": q,
        "mufassir": mufassir,
        "results": [],
        "quote": "Dan apabila hamba-hamba-Ku bertanya kepadamu tentang Aku, maka sesungguhnya Aku dekat. (QS. Al-Baqarah: 186)"
    }


# --- Ambil Tafsir per Ayat ---
@app.get("/api/v1/tafsir/{surah}/{ayah}", tags=["Tafsir"])
async def get_tafsir(surah: int, ayah: int, mufassir: str = "ibn-kathir"):
    """
    Ambil tafsir lengkap untuk suatu ayat spesifik.

    Parameter:
    - surah: Nomor surah (1-114)
    - ayah: Nomor ayat
    - mufassir: ID mufassir (default: ibn-kathir)
    """
    return {
        "surah": surah,
        "ayah": ayah,
        "mufassir": mufassir,
        "tafsir": "Tafsir akan dimuat dari sumber terverifikasi.",
        "quote": "Sesungguhnya Al-Qur'an ini memberi petunjuk ke jalan yang paling lurus. (QS. Al-Isra: 9)"
    }


# --- Analitik Tematik ---
@app.get("/api/v1/analytics/themes", tags=["Analitik"])
async def get_theme_analytics():
    """
    Analitik distribusi tema/topik dalam Al-Qur'an.
    """
    return {"themes": [], "total_categories": 0}


# --- Quotes Harian ---
@app.get("/api/v1/quotes/random", tags=["Quotes"])
async def get_random_quote():
    """
    Ambil quotes Al-Qur'an secara acak untuk inspirasi harian.
    """
    return {
        "text": "Sesungguhnya bersama kesulitan ada kemudahan. (QS. Al-Insyirah: 6)",
        "surah": "Al-Insyirah",
        "ayah": 6
    }


# --- Health Check ---
@app.get("/health", tags=["System"])
async def health_check():
    """Periksa status server."""
    return {"status": "Alhamdulillah, server berjalan normal", "uptime": "OK"}


# --- Root ---
@app.get("/", tags=["System"])
async def root():
    """Endpoint utama."""
    return {
        "project": "Quran Tafsir API",
        "version": "2.0.0",
        "docs": "/docs"
    }
