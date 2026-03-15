/**
 * Quran Tafsir - Halaman Utama
 *
 * Halaman utama platform pencarian tafsir Al-Qur'an.
 */
import { useState, useEffect } from "react";
import Head from "next/head";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface SearchResult {
  surah: number;
  ayah: number;
  text_arab?: string;
  terjemahan?: string;
  tafsir?: string;
  mufassir?: string;
}

interface Quote {
  text: string;
  surah: string;
  ayah: number;
}

export default function Home() {
  const [darkMode, setDarkMode] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [quote, setQuote] = useState<Quote | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeSection, setActiveSection] = useState("home");

  useEffect(() => {
    loadDailyQuote();
  }, []);

  async function loadDailyQuote() {
    try {
      const res = await fetch(`${API_BASE}/quotes/random`);
      if (res.ok) {
        const data = await res.json();
        setQuote(data);
      }
    } catch (e) {
      setQuote({
        text: "Sesungguhnya bersama kesulitan ada kemudahan.",
        surah: "Al-Insyirah",
        ayah: 6,
      });
    }
  }

  async function handleSearch() {
    if (!searchQuery.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(
        `${API_BASE}/search?q=${encodeURIComponent(searchQuery)}`
      );
      if (res.ok) {
        const data = await res.json();
        setResults(data.results || []);
      }
    } catch (e) {
      console.log("API belum aktif");
    }
    setLoading(false);
  }

  const bgClass = darkMode ? "bg-slate-950 text-slate-200" : "bg-white text-gray-900";
  const cardClass = darkMode
    ? "bg-slate-900/60 border-slate-800"
    : "bg-gray-50 border-gray-200";
  const mutedClass = darkMode ? "text-slate-500" : "text-gray-500";

  return (
    <div className={`min-h-screen ${bgClass}`}>
      <Head>
        <title>Quran Tafsir</title>
        <meta
          name="description"
          content="Platform pencarian tafsir Al-Qur'an yang terverifikasi dan tervalidasi"
        />
      </Head>

      {/* Navbar */}
      <nav className="sticky top-0 z-50 backdrop-blur border-b border-slate-800/50">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-emerald-400">QT</span>
            <div>
              <h1 className="font-bold text-emerald-400 text-lg leading-none">
                Quran Tafsir
              </h1>
              <p className={`text-xs ${mutedClass}`}>Terverifikasi</p>
            </div>
          </div>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="px-3 py-1.5 rounded-lg text-sm bg-gray-800 hover:bg-gray-700 transition"
          >
            {darkMode ? "Mode Terang" : "Mode Gelap"}
          </button>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-4 py-8">
        {/* Hero */}
        <div className="text-center mb-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-3">
            Pencarian Tafsir Al-Qur'an
          </h2>
          <p className="text-emerald-400 font-medium mb-2">
            Terverifikasi dan Tervalidasi
          </p>
          <p className={`${mutedClass} text-sm max-w-lg mx-auto`}>
            Cari tafsir dari berbagai mufassir terpercaya. Dilengkapi quotes
            Al-Qur'an yang relevan di setiap pencarian.
          </p>
        </div>

        {/* Search */}
        <div className="max-w-2xl mx-auto mb-8">
          <div className="flex gap-2">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              placeholder="Cari tafsir... (contoh: sabar, tawakkal, rezeki)"
              className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition"
            />
            <button
              onClick={handleSearch}
              disabled={loading}
              className="bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-3 rounded-xl text-sm font-medium transition"
            >
              Cari
            </button>
          </div>
        </div>

        {/* Daily Quote */}
        {quote && (
          <div className="max-w-2xl mx-auto mb-8">
            <div className={`${cardClass} border rounded-xl p-5`}>
              <p className="text-xs text-emerald-500 font-medium mb-3">
                <span className="text-lg mr-2">Ayat Harian</span>
              </p>
              <blockquote className="text-white font-medium italic text-sm leading-relaxed">
                &ldquo;{quote.text}&rdquo;
              </blockquote>
              <p className="text-emerald-600 text-xs mt-2">
                -- QS. {quote.surah}: {quote.ayah}
              </p>
            </div>
          </div>
        )}

        {/* Stats */}
        <div className="grid grid-cols-4 gap-3 max-w-2xl mx-auto mb-8">
          {[
            { label: "Surah", value: "114" },
            { label: "Ayat", value: "6.236" },
            { label: "Mufassir Verified", value: "10" },
            { label: "Cross-References", value: "40+" },
          ].map((stat, i) => (
            <div
              key={i}
              className={`text-center ${cardClass} border rounded-xl p-3`}
            >
              <p className="text-xl font-bold text-emerald-400">{stat.value}</p>
              <p className={`text-xs ${mutedClass} mt-1`}>{stat.label}</p>
            </div>
          ))}
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3 max-w-3xl mx-auto mt-8">
          {[
            {
              icon: "AT",
              name: "Analitik Tematik",
              desc: "Statistik distribusi tema dalam Al-Qur'an",
            },
            {
              icon: "AI",
              name: "Asisten AI",
              desc: "Asisten AI yang membantu memahami konteks ayat dengan merujuk tafsir ulama",
            },
            {
              icon: "KT",
              name: "Koneksi Tematik",
              desc: "Temukan keterkaitan antar ayat berdasarkan tema",
            },
            {
              icon: "AM",
              name: "Audio Murattal",
              desc: "Dengarkan bacaan Al-Qur'an dari qari pilihan (segera hadir)",
            },
            {
              icon: "CS",
              name: "Catatan Studi",
              desc: "Simpan catatan dan bookmark (segera hadir)",
            },
            {
              icon: "TP",
              name: "Tracking Progress",
              desc: "Pantau perkembangan belajar Al-Qur'an Anda",
            },
          ].map((feature, i) => (
            <div key={i} className={`${cardClass} border rounded-xl p-4`}>
              <p className="text-2xl mb-3 font-bold text-emerald-400">{feature.icon}</p>
              <p className="text-white text-sm font-medium">{feature.name}</p>
              <p className={`${mutedClass} text-xs mt-1`}>{feature.desc}</p>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 mt-12 py-6">
        <div className="max-w-5xl mx-auto px-4 text-center">
          <p className="text-gray-700 text-xs">
            Quran Tafsir -- Open Source untuk Umat
          </p>
        </div>
      </footer>
    </div>
  );
};
