"""
Quran Tafsir - Backend API

Server utama dengan data nyata dari equran.id API.
Manhaj: Ibnu Katsir, Jalalayn, Kemenag RI saja.
"""
import random
import time
import re
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx

# ----------------------------------------------------------------
# Inisialisasi Aplikasi
# ----------------------------------------------------------------
app = FastAPI(
    title="Quran Tafsir API",
    description="API untuk pencarian tafsir Al-Qur'an — Manhaj Salaf",
    version="3.0.0",
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

# ----------------------------------------------------------------
# Cache sederhana (in-memory dict)
# ----------------------------------------------------------------
_cache: dict = {}
CACHE_TTL = 3600  # 1 jam


def cache_get(key: str):
    entry = _cache.get(key)
    if entry and (time.time() - entry["ts"]) < CACHE_TTL:
        return entry["data"]
    return None


def cache_set(key: str, data):
    _cache[key] = {"data": data, "ts": time.time()}


# ----------------------------------------------------------------
# Helper: ambil data dari equran.id
# ----------------------------------------------------------------
EQURAN_BASE = "https://equran.id/api/v2"


async def fetch_equran(path: str):
    cached = cache_get(f"equran:{path}")
    if cached is not None:
        return cached
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{EQURAN_BASE}{path}")
            if resp.status_code == 200:
                data = resp.json().get("data")
                cache_set(f"equran:{path}", data)
                return data
    except Exception:
        pass
    return None


def strip_html(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text)


# ----------------------------------------------------------------
# SYNONYM DICTIONARY — seluas-luasnya
# ----------------------------------------------------------------
SYNONYMS = {
    # Variasi ejaan umum
    "shalat": ["salat", "sholat", "solat", "mendirikan salat", "tegakkan salat"],
    "tawakkal": ["tawakal", "bertawakal", "tawakul", "berserah diri", "berserah kepada allah"],
    "quran": ["qur'an", "alquran", "al-quran", "kitab", "kitabullah"],
    "zikir": ["dzikir", "zikr", "mengingat allah", "mengingat-ku"],
    "rezeki": ["rizki", "rizq", "riski", "karunia", "anugerah"],
    "zakat": ["zakat", "infak", "sedekah", "derma"],
    "jihad": ["jihad", "berjuang", "berjihad", "fisabilillah"],
    "syukur": ["bersyukur", "syukuri", "terima kasih kepada allah"],
    "istighfar": ["ampunan", "mohon ampun", "ampunilah", "pengampunan"],

    # Tema akidah
    "tauhid": ["esa", "menyekutukan", "keesaan allah", "tiada tuhan selain allah",
               "la ilaha illallah", "tidak ada sekutu"],
    "taubat": ["ampun", "istighfar", "kembali kepada allah", "bertaubat", "tobat"],
    "sabar": ["tabah", "teguh", "tidak berputus asa", "bersabarlah", "kesabaran"],
    "akhirat": ["hari kiamat", "hari pembalasan", "surga", "neraka", "hari akhir",
                "yaumul qiyamah", "kebangkitan"],
    "doa": ["memohon", "berdoa", "seruan", "munajat", "permohonan"],
    "akhlak": ["budi pekerti", "perilaku", "adab", "sopan santun", "mulia"],
    "keluarga": ["orang tua", "ibu bapak", "istri", "suami", "anak", "birrul walidain"],

    # Kisah para nabi
    "nabi ibrahim": ["ibrahim", "khalilullah", "bapak para nabi", "hanif"],
    "nabi musa": ["musa", "kalimullah", "bani israil", "firaun dan musa", "tongkat musa"],
    "nabi yusuf": ["yusuf", "putra yakub", "ibnu yaqub"],
    "nabi isa": ["isa", "almasih", "putra maryam", "ibnu maryam"],
    "nabi sulaiman": ["sulaiman", "nabi sulaiman", "ratu saba", "tentara sulaiman"],
    "nabi dawud": ["dawud", "zabur", "jalut dan dawud"],
    "nabi nuh": ["nuh", "banjir besar", "bahtera nuh", "kaum nuh"],
    "nabi adam": ["adam", "hawa", "surga adam", "iblis menggoda adam"],
    "nabi luth": ["luth", "kaum sodom", "kaum luth"],
    "nabi ayub": ["ayub", "kesabaran ayub", "penyakit ayub"],
    "nabi yunus": ["yunus", "dzun nun", "dzunnun", "perut ikan", "nun"],
    "nabi idris": ["idris", "diangkat derajatnya"],
    "nabi ismail": ["ismail", "putra ibrahim", "penyembelihan ismail"],
    "nabi ishaq": ["ishaq", "putra ibrahim"],
    "nabi yakub": ["yakub", "israil", "bapak yusuf"],
    "nabi zakariya": ["zakariya", "ayah yahya"],
    "nabi yahya": ["yahya", "putra zakariya"],

    # Kisah dalam Al-Qur'an
    "ashabul kahfi": ["penghuni gua", "pemuda gua", "tujuh pemuda"],
    "firaun": ["fir'aun", "firaun", "raja mesir", "penindas bani israil"],
    "qarun": ["qarun", "harta qarun", "kekayaan qarun", "sombong karena harta"],
    "maryam": ["maryam", "ibu isa", "wanita pilihan"],
    "ashabul fil": ["pasukan gajah", "abrahah", "burung ababil"],
    "luqman": ["luqman", "nasihat luqman", "luqman kepada anaknya"],
    "ashabul ukhdud": ["ukhdud", "parit berapi", "penguasa zalim"],
}


def expand_keywords(keyword: str) -> list[str]:
    """Perluas keyword menjadi daftar sinonim."""
    kw = keyword.lower().strip()
    keywords = [kw]

    # Cek exact match dulu
    if kw in SYNONYMS:
        keywords.extend(SYNONYMS[kw])
    else:
        # Cek partial match — kalau keyword ada di salah satu value
        for main_key, syns in SYNONYMS.items():
            if kw == main_key or kw in syns:
                keywords.append(main_key)
                keywords.extend(syns)
                break

    # Deduplicate sambil pertahankan urutan
    seen = set()
    unique = []
    for k in keywords:
        if k not in seen:
            seen.add(k)
            unique.append(k)
    return unique


# ----------------------------------------------------------------
# Quotes pilihan (fallback)
# ----------------------------------------------------------------
FALLBACK_QUOTES = [
    {"text": "Sesungguhnya bersama kesulitan ada kemudahan.", "surah": "Al-Insyirah", "ayah": 6},
    {"text": "Dan apabila hamba-hamba-Ku bertanya kepadamu tentang Aku, maka sesungguhnya Aku dekat.", "surah": "Al-Baqarah", "ayah": 186},
    {"text": "Barangsiapa bertakwa kepada Allah, niscaya Dia akan membukakan jalan keluar baginya.", "surah": "At-Talaq", "ayah": 2},
    {"text": "Allah tidak membebani seseorang melainkan sesuai dengan kesanggupannya.", "surah": "Al-Baqarah", "ayah": 286},
    {"text": "Dan Tuhanmu berfirman: Berdoalah kepada-Ku, niscaya akan Aku perkenankan bagimu.", "surah": "Ghafir", "ayah": 60},
    {"text": "Maka ingatlah kepada-Ku, niscaya Aku akan mengingat kalian.", "surah": "Al-Baqarah", "ayah": 152},
    {"text": "Sesungguhnya Al-Qur'an ini memberi petunjuk ke jalan yang paling lurus.", "surah": "Al-Isra", "ayah": 9},
    {"text": "Dan barangsiapa yang bertawakkal kepada Allah, niscaya Allah akan mencukupkan keperluannya.", "surah": "At-Talaq", "ayah": 3},
    {"text": "Dan Kami turunkan Al-Qur'an sebagai penawar dan rahmat bagi orang-orang yang beriman.", "surah": "Al-Isra", "ayah": 82},
    {"text": "Sesungguhnya Allah tidak akan mengubah keadaan suatu kaum hingga mereka mengubah keadaan yang ada pada diri mereka sendiri.", "surah": "Ar-Ra'd", "ayah": 11},
]

QUOTE_SURAHS = [1, 2, 3, 13, 14, 17, 20, 31, 36, 39, 40, 55, 65, 67, 93, 94, 103, 112, 113, 114]


# ----------------------------------------------------------------
# ENDPOINT: Pencarian (dengan Synonym Expansion)
# ----------------------------------------------------------------
@app.get("/api/v1/search", tags=["Pencarian"])
async def search_tafsir(
    q: str = Query(..., min_length=1, max_length=200, description="Kata kunci pencarian"),
):
    """
    Cari ayat yang mengandung keyword (+ sinonim) di terjemahan Indonesia.
    Mengambil tafsir Kemenag RI untuk setiap ayat yang ditemukan.
    """
    keyword = q.strip().lower()

    # Cek cache
    cache_key = f"search:{keyword}"
    cached = cache_get(cache_key)
    if cached is not None:
        return cached

    # Expand keywords dengan synonym
    all_keywords = expand_keywords(keyword)

    # Ambil daftar surah untuk mapping nama
    surah_list = await fetch_equran("/surat")
    surah_map = {}
    if surah_list:
        for s in surah_list:
            surah_map[s["nomor"]] = s

    results = []

    # Strategi: cari di surah-surah prioritas
    priority_surahs = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20,
                       21, 23, 24, 25, 29, 30, 31, 33, 35, 36, 39, 40, 41, 42, 46,
                       49, 51, 55, 56, 57, 59, 65, 67, 71, 73, 76, 78, 87, 89, 90,
                       91, 93, 94, 95, 96, 103, 109, 112, 113, 114]

    for surah_num in priority_surahs:
        if len(results) >= 15:
            break

        surah_data = await fetch_equran(f"/surat/{surah_num}")
        if not surah_data:
            continue

        surah_info = surah_map.get(surah_num, {})

        for ayat in surah_data.get("ayat", []):
            terjemahan = ayat.get("teksIndonesia", "")
            terjemahan_lower = terjemahan.lower()

            # Cek apakah salah satu keyword cocok
            matched = any(kw in terjemahan_lower for kw in all_keywords)
            if not matched:
                continue

            # Ambil tafsir Kemenag RI
            tafsir_text = ""
            tafsir_data = await fetch_equran(f"/tafsir/{surah_num}")
            if tafsir_data:
                for t in tafsir_data.get("tafsir", []):
                    if t.get("ayat") == ayat.get("nomorAyat"):
                        raw = t.get("teks", "")
                        tafsir_text = strip_html(raw)
                        break

            results.append({
                "surah": surah_num,
                "ayah": ayat.get("nomorAyat"),
                "surah_name": surah_info.get("namaLatin", f"Surah {surah_num}"),
                "text_arab": ayat.get("teksArab", ""),
                "terjemahan": terjemahan,
                "tafsir_list": [
                    {"name": "Kemenag RI", "text": tafsir_text}
                ] if tafsir_text else [],
            })

            if len(results) >= 15:
                break

    # Quote relevan
    quote_text = ""
    if results:
        pick = random.choice(results)
        quote_text = f"{pick['terjemahan']} (QS. {pick['surah_name']}: {pick['ayah']})"
    else:
        fb = random.choice(FALLBACK_QUOTES)
        quote_text = f"{fb['text']} (QS. {fb['surah']}: {fb['ayah']})"

    response = {
        "query": q,
        "total_results": len(results),
        "results": results,
        "quote": quote_text,
    }

    cache_set(cache_key, response)
    return response


# ----------------------------------------------------------------
# ENDPOINT: Tafsir per Ayat
# ----------------------------------------------------------------
@app.get("/api/v1/tafsir/{surah}/{ayah}", tags=["Tafsir"])
async def get_tafsir(surah: int, ayah: int):
    """Ambil tafsir untuk surah dan ayat tertentu."""
    if surah < 1 or surah > 114:
        return {"error": "Nomor surah harus antara 1 dan 114"}

    surah_data = await fetch_equran(f"/surat/{surah}")
    ayat_data = None
    if surah_data:
        for a in surah_data.get("ayat", []):
            if a.get("nomorAyat") == ayah:
                ayat_data = a
                break

    tafsir_text = ""
    tafsir_data = await fetch_equran(f"/tafsir/{surah}")
    if tafsir_data:
        for t in tafsir_data.get("tafsir", []):
            if t.get("ayat") == ayah:
                tafsir_text = strip_html(t.get("teks", ""))
                break

    return {
        "surah": surah,
        "ayah": ayah,
        "surah_name": surah_data.get("namaLatin", "") if surah_data else "",
        "text_arab": ayat_data.get("teksArab", "") if ayat_data else "",
        "text_latin": ayat_data.get("teksLatin", "") if ayat_data else "",
        "terjemahan": ayat_data.get("teksIndonesia", "") if ayat_data else "",
        "tafsir": tafsir_text,
        "tafsir_source": "Kemenag RI",
    }


# ----------------------------------------------------------------
# ENDPOINT: Quotes Random
# ----------------------------------------------------------------
@app.get("/api/v1/quotes/random", tags=["Quotes"])
async def get_random_quote():
    """Ambil satu ayat acak dari Al-Qur'an sebagai quote."""
    surah_num = random.choice(QUOTE_SURAHS)
    surah_data = await fetch_equran(f"/surat/{surah_num}")
    if surah_data and surah_data.get("ayat"):
        ayat_list = surah_data["ayat"]
        pick = random.choice(ayat_list)
        return {
            "text": pick.get("teksIndonesia", ""),
            "surah": surah_data.get("namaLatin", ""),
            "ayah": pick.get("nomorAyat", 0),
        }
    return random.choice(FALLBACK_QUOTES)


# ----------------------------------------------------------------
# ENDPOINT: Quotes Harian
# ----------------------------------------------------------------
@app.get("/api/v1/quotes/daily", tags=["Quotes"])
async def get_daily_quote():
    """Ambil ayat harian (konsisten per hari)."""
    from datetime import date
    today = date.today()
    seed = today.year * 10000 + today.month * 100 + today.day
    rng = random.Random(seed)

    surah_num = rng.choice(QUOTE_SURAHS)
    surah_data = await fetch_equran(f"/surat/{surah_num}")
    if surah_data and surah_data.get("ayat"):
        ayat_list = surah_data["ayat"]
        pick = rng.choice(ayat_list)
        return {
            "text": pick.get("teksIndonesia", ""),
            "surah": surah_data.get("namaLatin", ""),
            "ayah": pick.get("nomorAyat", 0),
            "date": str(today),
        }

    fb = rng.choice(FALLBACK_QUOTES)
    fb["date"] = str(today)
    return fb


# ----------------------------------------------------------------
# ENDPOINT: Daftar Mufassir
# ----------------------------------------------------------------
@app.get("/api/v1/mufassireen", tags=["Tafsir"])
async def list_mufassireen():
    """Daftar mufassir yang tersedia."""
    return {
        "total": 3,
        "mufassireen": [
            {
                "id": "ibnu-katsir",
                "name": "Imam Ibnu Katsir",
                "kitab": "Tafsir Al-Qur'an Al-Azhim",
                "description": "Tafsir bil Ma'tsur — mengutamakan Al-Qur'an, Hadits Shahih, Atsar Sahabat",
                "era": "700-774 H / 1300-1373 M",
                "badge": "Rujukan Utama Ahlus Sunnah",
            },
            {
                "id": "jalalayn",
                "name": "Tafsir Jalalayn",
                "kitab": "Tafsir al-Jalalayn",
                "description": "Ringkas, padat, berbasis riwayat",
                "era": "Jalaluddin Al-Mahalli & Jalaluddin As-Suyuthi",
                "badge": "Tafsir Ringkas Mu'tamad",
            },
            {
                "id": "kemenag",
                "name": "Tafsir Kemenag RI",
                "kitab": "Tafsir Kemenag",
                "description": "Tafsir resmi negara, pendekatan kontekstual Indonesia",
                "era": "Kontemporer",
                "badge": "Referensi Resmi Indonesia",
            },
        ],
        "note": "Hanya tafsir yang terverifikasi sesuai manhaj salaf.",
    }


# ----------------------------------------------------------------
# ENDPOINT: Health Check
# ----------------------------------------------------------------
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "Alhamdulillah, server berjalan normal", "uptime": "OK"}


@app.get("/", tags=["System"])
async def root():
    return {
        "project": "Quran Tafsir API",
        "version": "3.0.0",
        "docs": "/docs",
        "source": "Data dari equran.id (Kemenag RI) | Manhaj Salaf",
    }
