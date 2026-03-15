"""
Database Mufassir (Penulis Tafsir) Terverifikasi

Daftar para mufassir yang kitab tafsirnya diakui dan diterima
oleh ulama Ahlus Sunnah wal Jama'ah.
"""

MUFASSIREEN = [
    {
        "id": "ibn-kathir",
        "name": "Ibnu Katsir",
        "full_name": "Isma'il bin Umar bin Katsir Al-Qurasyi Ad-Dimasyqi",
        "era": "701-774 H (1301-1373 M)",
        "kitab": "Tafsir Al-Qur'an Al-'Azhim",
        "method": "Bil Ma'tsur (berdasarkan riwayat)",
        "api_id": 1,
        "description": (
            "Salah satu tafsir paling terkenal dan paling banyak dirujuk. "
            "Metodenya menafsirkan Al-Qur'an dengan Al-Qur'an, kemudian dengan hadits, "
            "kemudian dengan pendapat sahabat dan tabi'in. "
            "Sumber utamanya adalah Al-Qur'an, hadits, dan atsar para ulama terdahulu."
        ),
        "manhaj_notes": (
            "Berpegang teguh pada akidah Ahlus Sunnah. Murid senior dari "
            "Syaikhul Islam Ibnu Taimiyah."
        ),
    },
    {
        "id": "as-sadi",
        "name": "As-Sa'di",
        "full_name": "Abdurrahman bin Nashir As-Sa'di",
        "era": "1307-1376 H (1889-1956 M)",
        "kitab": "Taisir Al-Karim Ar-Rahman",
        "method": "Gabungan Riwayat dan Analisis",
        "api_id": 2,
        "description": (
            "Tafsir kontemporer yang sangat mudah dipahami. "
            "Bahasanya ringkas dan langsung ke inti makna ayat. "
            "Banyak dipakai di berbagai lembaga pendidikan Islam."
        ),
        "manhaj_notes": (
            "Berpegang pada akidah Ahlus Sunnah. Tafsirnya mudah "
            "dipahami oleh kalangan umum dan pelajar."
        ),
    },
    {
        "id": "al-tabari",
        "name": "At-Tabari",
        "full_name": "Muhammad bin Jarir At-Tabari",
        "era": "224-310 H (839-923 M)",
        "kitab": "Jami' Al-Bayan fi Ta'wil Al-Qur'an",
        "method": "Bil Ma'tsur (berdasarkan riwayat)",
        "api_id": 3,
        "description": (
            "Tafsir paling komprehensif dari sisi riwayat. "
            "Mengumpulkan semua pendapat ulama terdahulu untuk setiap ayat, "
            "lalu memilih pendapat yang paling kuat berdasarkan kaidah ilmiah."
        ),
        "manhaj_notes": (
            "Imam besar dalam tafsir bil ma'tsur. Mengumpulkan pendapat "
            "para ulama terdahulu secara lengkap dengan analisis kritis."
        ),
    },
    {
        "id": "al-baghawi",
        "name": "Al-Baghawi",
        "full_name": "Al-Husain bin Mas'ud Al-Baghawi",
        "era": "436-516 H (1044-1122 M)",
        "kitab": "Ma'alim At-Tanzil",
        "method": "Bil Ma'tsur (berdasarkan riwayat)",
        "api_id": 4,
        "description": (
            "Dikenal sebagai 'Muhyis Sunnah' (penghidup sunnah). "
            "Tafsirnya ringkas tapi padat isi, mengutip riwayat-riwayat terpilih."
        ),
        "manhaj_notes": (
            "Berpegang pada akidah Ahlus Sunnah. Tafsirnya mudah "
            "dipahami oleh kalangan umum dan pelajar."
        ),
    },
    {
        "id": "ibn-rajab",
        "name": "Ibnu Rajab",
        "full_name": "Zainuddin Abdurrahman bin Ahmad bin Rajab Al-Hanbali",
        "era": "736-795 H (1335-1393 M)",
        "kitab": "Tafsir Ibnu Rajab Al-Hanbali",
        "method": "Bil Ma'tsur dengan pendalaman fiqh",
        "api_id": None,
        "description": (
            "Dikenal dengan kedalaman pemahaman hadits dan fiqh. "
            "Penjelasannya sangat detail terutama dalam aspek hukum fiqih."
        ),
        "manhaj_notes": (
            "Ulama Hanbali yang berpegang pada akidah Ahlus Sunnah. "
            "Banyak merujuk pada pendapat Ibnu Taimiyah."
        ),
    },
    {
        "id": "as-shanqiti",
        "name": "Asy-Syanqithi",
        "full_name": "Muhammad Al-Amin bin Muhammad Al-Mukhtar Asy-Syanqithi",
        "era": "1325-1393 H (1907-1973 M)",
        "kitab": "Adhwa' Al-Bayan fi Idhah Al-Qur'an bil Qur'an",
        "method": "Tafsir Al-Qur'an dengan Al-Qur'an",
        "api_id": None,
        "description": (
            "Metode uniknya adalah menafsirkan Al-Qur'an dengan Al-Qur'an itu sendiri. "
            "Menghubungkan ayat-ayat yang saling menjelaskan secara detail."
        ),
        "manhaj_notes": (
            "Berpegang pada akidah Ahlus Sunnah dan disetujui oleh "
            "Hai'ah Kibar Al-Ulama (Dewan Ulama Senior)."
        ),
    },
    {
        "id": "ibn-abi-hatim",
        "name": "Ibnu Abi Hatim",
        "full_name": "Abdurrahman bin Muhammad bin Idris Ar-Razi",
        "era": "240-327 H (854-938 M)",
        "kitab": "Tafsir Al-Qur'an Al-'Azhim (Ibnu Abi Hatim)",
        "method": "Bil Ma'tsur murni",
        "api_id": None,
        "description": (
            "Tafsir bil ma'tsur murni yang hanya berisi riwayat tanpa analisis tambahan. "
            "Sumber utama untuk mengetahui pendapat sahabat dan tabi'in."
        ),
        "manhaj_notes": (
            "Ahli hadits tingkat tinggi. Tafsirnya murni berisi riwayat "
            "dari sahabat dan tabi'in."
        ),
    },
    {
        "id": "ibn-al-qayyim",
        "name": "Ibnul Qayyim",
        "full_name": "Muhammad bin Abi Bakr bin Ayyub (Ibnul Qayyim Al-Jauziyah)",
        "era": "691-751 H (1292-1350 M)",
        "kitab": "At-Tibyan fi Aqsam Al-Qur'an / Bada'i At-Tafsir",
        "method": "Analisis mendalam per tema",
        "api_id": None,
        "description": (
            "Bukan tafsir lengkap 30 juz, tapi kumpulan analisis mendalam "
            "terhadap ayat-ayat tertentu terutama berkaitan dengan akidah dan tauhid."
        ),
        "manhaj_notes": (
            "Murid utama Syaikhul Islam Ibnu Taimiyah. Sangat kuat dalam "
            "membedah ayat-ayat yang berkaitan dengan sifat Allah."
        ),
    },
    {
        "id": "ibn-abbas",
        "name": "Ibnu Abbas",
        "full_name": "Abdullah bin Abbas bin Abdul Muthalib",
        "era": "3 SH - 68 H (619-687 M)",
        "kitab": "Tanwir Al-Miqbas min Tafsir Ibn Abbas",
        "method": "Tafsir Sahabat",
        "api_id": None,
        "description": (
            "Sepupu Nabi shallallahu 'alaihi wa sallam, dikenal sebagai "
            "'Turjumanul Qur'an' (penerjemah Al-Qur'an). "
            "Sahabat yang paling paham tentang tafsir."
        ),
        "manhaj_notes": (
            "Sahabat Nabi shallallahu 'alaihi wa sallam, dikenal sebagai "
            "'Turjumanul Qur'an'. Penafsirannya menjadi rujukan utama."
        ),
    },
    {
        "id": "al-uthaymeen",
        "name": "Ibnu Utsaimin",
        "full_name": "Muhammad bin Shalih Al-Utsaimin",
        "era": "1347-1421 H (1929-2001 M)",
        "kitab": "Tafsir Al-Qur'an Al-Karim",
        "method": "Penjelasan kontemporer berbasis ilmu",
        "api_id": None,
        "description": (
            "Ulama kontemporer yang sangat detail dalam menjelaskan ayat "
            "dengan bahasa yang mudah dipahami. Banyak membahas faidah dan "
            "pelajaran praktis dari setiap ayat."
        ),
        "manhaj_notes": (
            "Ulama besar kontemporer yang diakui keilmuannya. "
            "Penjelasannya sangat mudah dipahami oleh semua kalangan."
        ),
    },
]
