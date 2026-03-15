"""
Database Quotes Al-Qur'an

Kumpulan ayat-ayat pilihan yang sering dicari dan relevan untuk ditampilkan
sebagai quotes inspiratif.
"""

QURAN_QUOTES = [
    {
        "text": "Sesungguhnya bersama kesulitan ada kemudahan.",
        "surah": "Al-Insyirah",
        "ayah": 6,
        "theme": "sabar",
    },
    {
        "text": "Dan apabila hamba-hamba-Ku bertanya kepadamu (Muhammad) tentang Aku, maka sesungguhnya Aku dekat.",
        "surah": "Al-Baqarah",
        "ayah": 186,
        "theme": "doa",
    },
    {
        "text": "Barangsiapa bertakwa kepada Allah, niscaya Dia akan membukakan jalan keluar baginya.",
        "surah": "At-Talaq",
        "ayah": 2,
        "theme": "tawakkal",
    },
    {
        "text": "Sesungguhnya Allah tidak akan mengubah keadaan suatu kaum hingga mereka mengubah keadaan yang ada pada diri mereka sendiri.",
        "surah": "Ar-Ra'd",
        "ayah": 11,
        "theme": "ikhtiar",
    },
    {
        "text": "Dan Tuhanmu berfirman: Berdoalah kepada-Ku, niscaya akan Aku perkenankan bagimu.",
        "surah": "Ghafir",
        "ayah": 60,
        "theme": "doa",
    },
    {
        "text": "Maka ingatlah kepada-Ku, niscaya Aku akan mengingat kalian.",
        "surah": "Al-Baqarah",
        "ayah": 152,
        "theme": "dzikir",
    },
    {
        "text": "Dan barangsiapa yang bertawakkal kepada Allah, niscaya Allah akan mencukupkan keperluannya.",
        "surah": "At-Talaq",
        "ayah": 3,
        "theme": "tawakkal",
    },
    {
        "text": "Sesungguhnya Al-Qur'an ini memberi petunjuk ke jalan yang paling lurus.",
        "surah": "Al-Isra",
        "ayah": 9,
        "theme": "hidayah",
    },
    {
        "text": "Allah tidak membebani seseorang melainkan sesuai dengan kesanggupannya.",
        "surah": "Al-Baqarah",
        "ayah": 286,
        "theme": "sabar",
    },
    {
        "text": "Dan Kami turunkan Al-Qur'an sebagai penawar dan rahmat bagi orang-orang yang beriman.",
        "surah": "Al-Isra",
        "ayah": 82,
        "theme": "syifa",
    },
]


def get_random_quote():
    """Ambil satu quotes acak dari database."""
    import random
    return random.choice(QURAN_QUOTES)


def get_quotes_by_theme(theme: str):
    """Ambil quotes berdasarkan tema tertentu."""
    return [q for q in QURAN_QUOTES if q["theme"] == theme]
