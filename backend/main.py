"""
Quran Tafsir - Backend API

Server utama dengan data nyata dari equran.id API + tafsir dari CDN dan quran.com.
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
    version="3.1.0",
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
# TAFSIR CACHE — Jalalayn & Kemenag (loaded at startup)
# ----------------------------------------------------------------
TAFSIR_CACHE = {
    "jalalayn": {},
    "kemenag": {},
}
IBNU_KATSIR_CACHE: dict = {}


async def load_tafsir_data():
    """Load Jalalayn & Kemenag data from CDN at startup."""
    urls = {
        "jalalayn": "https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/ind-jalaladdinalmah.min.json",
        "kemenag": "https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/ind-indonesianislam.min.json",
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        for name, url in urls.items():
            try:
                res = await client.get(url)
                data = res.json()
                for item in data["quran"]:
                    key = f"{item['chapter']}:{item['verse']}"
                    TAFSIR_CACHE[name][key] = item["text"]
                print(f"[STARTUP] Loaded {name}: {len(TAFSIR_CACHE[name])} ayat")
            except Exception as e:
                print(f"[STARTUP ERROR] Failed to load {name}: {e}")


@app.on_event("startup")
async def startup_event():
    await load_tafsir_data()


# ----------------------------------------------------------------
# Helper: Ibnu Katsir per-ayat (from quran.com API v4)
# ----------------------------------------------------------------
async def fetch_ibnu_katsir(surah: int, ayah: int) -> str:
    """Fetch Ibnu Katsir tafsir (English) for a single ayah.
    Uses quran.com API v4, resource_id 169 (Ibn Kathir abridged).
    Returns plain text (HTML stripped) or empty string on failure."""
    cache_key = f"{surah}:{ayah}"
    if cache_key in IBNU_KATSIR_CACHE:
        return IBNU_KATSIR_CACHE[cache_key]

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"https://api.quran.com/api/v4/tafsirs/169/by_ayah/{surah}:{ayah}"
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                raw_html = data.get("tafsir", {}).get("text", "")
                # Strip HTML tags
                text = strip_html_bs(raw_html)
                IBNU_KATSIR_CACHE[cache_key] = text
                return text
    except Exception:
        pass
    return ""


def strip_html_bs(html_text: str) -> str:
    """Strip HTML tags using BeautifulSoup (more robust than regex for nested HTML)."""
    if not html_text:
        return ""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_text, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except ImportError:
        # Fallback to regex if bs4 not installed
        return re.sub(r"<[^>]+>", "", html_text).strip()


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
# Helper: build tafsir_list for an ayah (all 3 sources)
# ----------------------------------------------------------------
async def build_tafsir_list(surah: int, ayah: int) -> list:
    """Assemble tafsir from all 3 verified sources for a given ayah."""
    key = f"{surah}:{ayah}"
    tafsir_list = []

    # 1. Ibnu Katsir (English) — per-ayat API call
    ik_text = await fetch_ibnu_katsir(surah, ayah)
    if ik_text:
        tafsir_list.append({
            "name": "Ibnu Katsir (English)",
            "sub_label": "Abridged · Hafiz Ibn Kathir",
            "text": ik_text,
        })

    # 2. Jalalayn (Indonesian) — from pre-loaded cache
    jal_text = TAFSIR_CACHE["jalalayn"].get(key, "")
    if jal_text:
        tafsir_list.append({
            "name": "Jalalayn",
            "sub_label": "",
            "text": jal_text,
        })

    # 3. Kemenag RI (Indonesian) — from pre-loaded cache
    kem_text = TAFSIR_CACHE["kemenag"].get(key, "")
    if kem_text:
        tafsir_list.append({
            "name": "Kemenag RI",
            "sub_label": "",
            "text": kem_text,
        })

    return tafsir_list


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
# ENDPOINT: Pencarian (dengan Synonym Expansion + 3 Tafsir)
# ----------------------------------------------------------------
@app.get("/api/v1/search", tags=["Pencarian"])
async def search_tafsir(
    q: str = Query(..., min_length=1, max_length=200, description="Kata kunci pencarian"),
):
    """
    Cari ayat yang mengandung keyword (+ sinonim) di terjemahan Indonesia.
    Mengambil tafsir dari 3 sumber: Ibnu Katsir (English), Jalalayn, Kemenag RI.
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

            ayah_num = ayat.get("nomorAyat")

            # Build tafsir list from all 3 sources
            tafsir_list = await build_tafsir_list(surah_num, ayah_num)

            results.append({
                "surah": surah_num,
                "ayah": ayah_num,
                "surah_name": surah_info.get("namaLatin", f"Surah {surah_num}"),
                "text_arab": ayat.get("teksArab", ""),
                "terjemahan": terjemahan,
                "tafsir_list": tafsir_list,
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
# ENDPOINT: Tafsir per Ayat (all 3 sources)
# ----------------------------------------------------------------
@app.get("/api/v1/tafsir/{surah}/{ayah}", tags=["Tafsir"])
async def get_tafsir(surah: int, ayah: int):
    """Ambil tafsir dari 3 sumber untuk surah dan ayat tertentu."""
    if surah < 1 or surah > 114:
        return {"error": "Nomor surah harus antara 1 dan 114"}

    surah_data = await fetch_equran(f"/surat/{surah}")
    ayat_data = None
    if surah_data:
        for a in surah_data.get("ayat", []):
            if a.get("nomorAyat") == ayah:
                ayat_data = a
                break

    tafsir_list = await build_tafsir_list(surah, ayah)

    return {
        "surah": surah,
        "ayah": ayah,
        "surah_name": surah_data.get("namaLatin", "") if surah_data else "",
        "text_arab": ayat_data.get("teksArab", "") if ayat_data else "",
        "text_latin": ayat_data.get("teksLatin", "") if ayat_data else "",
        "terjemahan": ayat_data.get("teksIndonesia", "") if ayat_data else "",
        "tafsir_list": tafsir_list,
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
                "language": "English (Abridged)",
            },
            {
                "id": "jalalayn",
                "name": "Tafsir Jalalayn",
                "kitab": "Tafsir al-Jalalayn",
                "description": "Ringkas, padat, berbasis riwayat",
                "era": "Jalaluddin Al-Mahalli & Jalaluddin As-Suyuthi",
                "badge": "Tafsir Ringkas Mu'tamad",
                "language": "Bahasa Indonesia",
            },
            {
                "id": "kemenag",
                "name": "Tafsir Kemenag RI",
                "kitab": "Tafsir Kemenag",
                "description": "Tafsir resmi negara, pendekatan kontekstual Indonesia",
                "era": "Kontemporer",
                "badge": "Referensi Resmi Indonesia",
                "language": "Bahasa Indonesia",
            },
        ],
        "note": "Hanya tafsir yang terverifikasi sesuai manhaj salaf.",
    }


# ----------------------------------------------------------------
# ENDPOINT: Health Check
# ----------------------------------------------------------------
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "Alhamdulillah, server berjalan normal",
        "uptime": "OK",
        "tafsir_jalalayn_loaded": len(TAFSIR_CACHE["jalalayn"]),
        "tafsir_kemenag_loaded": len(TAFSIR_CACHE["kemenag"]),
        "ibnu_katsir_cached": len(IBNU_KATSIR_CACHE),
    }


@app.get("/", tags=["System"])
async def root():
    return {
        "project": "Quran Tafsir API",
        "version": "3.1.0",
        "docs": "/docs",
        "source": "Ibnu Katsir (quran.com) + Jalalayn & Kemenag (CDN) | Manhaj Salaf",
    }
