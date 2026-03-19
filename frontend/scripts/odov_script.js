// ============================================================
// ONE DAY ONE VERSE — Frontend Logic
// Tambahkan di bagian bawah <body> atau file JS terpisah
// ============================================================

(function () {
  const API_BASE  = 'https://tafseer.my.id/api/v1'; // ganti sesuai domain
  const SEED_KEY  = 'odov_user_seed';
  const STATE_KEY = 'odov_state';

  // Elemen DOM
  const backdrop   = document.getElementById('odov-backdrop');
  const popup      = document.getElementById('odov-popup');
  const loader     = document.getElementById('odov-loader');
  const content    = document.getElementById('odov-content');
  const errorEl    = document.getElementById('odov-error');
  const closeBtn   = document.getElementById('odov-close');
  const retryBtn   = document.getElementById('odov-retry');
  const regenBtn   = document.getElementById('odov-regenerate');
  const shareBtn   = document.getElementById('odov-share');
  const tafsirToggle = document.getElementById('odov-tafsir-toggle');
  const tafsirBody   = document.getElementById('odov-tafsir-body');
  const chevron      = tafsirToggle.querySelector('.odov-chevron');

  // State
  let currentData = null;
  let offset = 0;

  // ── Seed unik per user (persisten) ──
  function getUserSeed() {
    let seed = localStorage.getItem(SEED_KEY);
    if (!seed) {
      seed = Math.floor(Math.random() * 99999);
      localStorage.setItem(SEED_KEY, seed);
    }
    return parseInt(seed);
  }

  // ── Cache harian (reset tiap hari) ──
  function getTodayKey() {
    const d = new Date();
    return `odov_${d.getFullYear()}_${d.getMonth()}_${d.getDate()}`;
  }

  function getCachedState(key) {
    try {
      const raw = sessionStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch { return null; }
  }

  function setCachedState(key, data) {
    try { sessionStorage.setItem(key, JSON.stringify(data)); } catch {}
  }

  // ── Fetch ayat ──
  async function fetchVerse(userOffset = 0) {
    const seed = getUserSeed();
    const url  = `${API_BASE}/odov?seed=${seed}&offset=${userOffset}`;
    const res  = await fetch(url);
    if (!res.ok) throw new Error('Network error');
    return res.json();
  }

  // ── Apply palette ke popup ──
  function applyPalette(palette) {
    if (!palette) return;
    popup.style.setProperty('--odov-from', palette.from);
    popup.style.setProperty('--odov-via',  palette.via);
    popup.style.setProperty('--odov-to',   palette.to);
    popup.style.setProperty('--odov-text', palette.text);
    popup.style.color = palette.text;
  }

  // ── Render data ke DOM ──
  function renderVerse(data) {
    currentData = data;
    const v = data.verse;

    applyPalette(data.palette);

    document.getElementById('odov-theme-badge').textContent = v.theme_label || '';
    document.getElementById('odov-hook').textContent        = v.genz_hook   || '';
    document.getElementById('odov-arab').textContent        = v.text_arab   || '';
    document.getElementById('odov-latin').textContent       = v.text_latin  || '';
    document.getElementById('odov-terjemahan').textContent  = v.terjemahan_id || v.translation_en || '';

    const ref = `QS. ${v.surah_name || 'Surah ' + v.surah} : ${v.ayah}`;
    document.getElementById('odov-surah-info').textContent = ref;

    // Tafsir
    const tafsirList = document.getElementById('odov-tafsir-list');
    tafsirList.innerHTML = '';
    (data.tafsir_list || []).forEach(t => {
      const item = document.createElement('div');
      item.className = 'odov-tafsir-item';

      const textId = `tafsir-text-${Math.random().toString(36).slice(2)}`;
      item.innerHTML = `
        <div class="odov-tafsir-name">${t.name}${t.sub_label ? ' · ' + t.sub_label : ''}</div>
        <div class="odov-tafsir-text" id="${textId}">${escHtml(t.text || '')}</div>
        <button class="odov-tafsir-readmore" data-target="${textId}">Baca selengkapnya ▾</button>
      `;
      tafsirList.appendChild(item);
    });

    // Readmore handler
    tafsirList.querySelectorAll('.odov-tafsir-readmore').forEach(btn => {
      btn.addEventListener('click', () => {
        const el = document.getElementById(btn.dataset.target);
        el.classList.toggle('expanded');
        btn.textContent = el.classList.contains('expanded') ? 'Sembunyikan ▴' : 'Baca selengkapnya ▾';
      });
    });

    // Meta
    const meta = data.meta || {};
    const canRegen = meta.can_regenerate !== false;
    document.getElementById('odov-meta').textContent =
      canRegen
        ? `Refresh ${offset}/20 kali hari ini · ${data.date || ''}`
        : `Batas refresh hari ini tercapai · ${data.date || ''}`;

    regenBtn.disabled = !canRegen;
    regenBtn.style.opacity = canRegen ? '1' : '0.4';
  }

  function escHtml(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  // ── Show / Hide ──
  function showLoader() {
    loader.classList.remove('hidden');
    content.classList.add('hidden');
    errorEl.classList.add('hidden');
  }

  function showContent() {
    loader.classList.add('hidden');
    content.classList.remove('hidden');
    errorEl.classList.add('hidden');
  }

  function showError() {
    loader.classList.add('hidden');
    content.classList.add('hidden');
    errorEl.classList.remove('hidden');
  }

  function openPopup() {
    backdrop.classList.remove('hidden');
    popup.classList.remove('hidden');
    backdrop.removeAttribute('aria-hidden');
    document.body.style.overflow = 'hidden';
    loadVerse();
  }

  function closePopup() {
    backdrop.classList.add('hidden');
    popup.classList.add('hidden');
    backdrop.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  // ── Load verse (dengan daily cache) ──
  async function loadVerse(forceOffset = null) {
    const todayKey = getTodayKey();
    const useOffset = forceOffset !== null ? forceOffset : offset;

    if (useOffset === 0) {
      const cached = getCachedState(todayKey);
      if (cached) {
        renderVerse(cached);
        showContent();
        return;
      }
    }

    showLoader();
    try {
      const data = await fetchVerse(useOffset);
      if (useOffset === 0) setCachedState(todayKey, data);
      renderVerse(data);
      showContent();
    } catch (e) {
      console.error('[ODOV]', e);
      showError();
    }
  }

  // ── Event Listeners ──
  closeBtn.addEventListener('click', closePopup);
  backdrop.addEventListener('click', closePopup);

  retryBtn.addEventListener('click', () => loadVerse(offset));

  regenBtn.addEventListener('click', () => {
    if (offset >= 20) return;
    offset++;
    loadVerse(offset);
  });

  shareBtn.addEventListener('click', async () => {
    if (!currentData) return;
    const v    = currentData.verse;
    const text = `"${v.terjemahan_id || v.translation_en}"\n— QS. ${v.surah_name}: ${v.ayah}\n\n#QuranHarian #TafseerApp`;
    if (navigator.share) {
      await navigator.share({ title: 'Ayat Hari Ini', text });
    } else {
      await navigator.clipboard.writeText(text);
      shareBtn.textContent = '✅ Disalin!';
      setTimeout(() => { shareBtn.textContent = '📤 Bagikan'; }, 2000);
    }
  });

  tafsirToggle.addEventListener('click', () => {
    tafsirBody.classList.toggle('hidden');
    chevron.classList.toggle('open');
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closePopup();
  });

  // ── Expose API global ──
  window.ODOV = {
    open:  openPopup,
    close: closePopup,
  };

  // ── Auto-trigger tombol pemicu ──
  document.querySelectorAll('[data-odov-trigger]').forEach(el => {
    el.addEventListener('click', openPopup);
  });

})();
