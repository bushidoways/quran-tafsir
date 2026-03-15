#!/bin/bash
# ================================================================
# Script Deployment Otomatis: Quran Tafsir → tafseer.my.id
# ================================================================
# Jalankan di VPS sebagai user 'tafseer':
#   chmod +x deploy.sh && sudo ./deploy.sh
#
# Prasyarat:
#   - Ubuntu 22.04 LTS
#   - User: tafseer
#   - Domain: tafseer.my.id
#   - Repo: https://github.com/bushidoways/quran-tafsir
# ================================================================

set -e  # Berhenti jika ada error

# --- Variabel ---
DOMAIN="tafseer.my.id"
PROJECT_DIR="/var/www/tafseer"
REPO_URL="https://github.com/bushidoways/quran-tafsir.git"
APP_USER="tafseer"
PYTHON_VERSION="3.12"

echo ""
echo "========================================"
echo "  DEPLOYMENT QURAN TAFSIR"
echo "  Domain: $DOMAIN"
echo "========================================"
echo ""

# --- Pastikan dijalankan sebagai root ---
if [ "$EUID" -ne 0 ]; then
  echo "GAGAL: Script ini harus dijalankan dengan sudo."
  echo "Gunakan: sudo ./deploy.sh"
  exit 1
fi

# ================================================================
# LANGKAH 1: Update System
# ================================================================
echo "[1/7] Mengupdate system..."
apt update -y
apt upgrade -y
echo "      System berhasil diupdate."

# ================================================================
# LANGKAH 2: Install Dependencies
# ================================================================
echo ""
echo "[2/7] Menginstall dependencies..."

# Install software-properties-common untuk add-apt-repository
apt install -y software-properties-common

# Tambah deadsnakes PPA untuk Python 3.12
add-apt-repository -y ppa:deadsnakes/ppa
apt update -y

# Install semua yang dibutuhkan
apt install -y \
  git \
  python${PYTHON_VERSION} \
  python${PYTHON_VERSION}-venv \
  python${PYTHON_VERSION}-dev \
  python3-pip \
  nginx \
  certbot \
  python3-certbot-nginx \
  curl \
  ufw

echo "      Dependencies berhasil diinstall."

# Verifikasi
echo "      Python version: $(python${PYTHON_VERSION} --version)"
echo "      Nginx version: $(nginx -v 2>&1)"
echo "      Git version: $(git --version)"

# ================================================================
# LANGKAH 3: Setup Firewall
# ================================================================
echo ""
echo "[3/7] Mengkonfigurasi firewall..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable
echo "      Firewall aktif. Port SSH, HTTP, dan HTTPS terbuka."

# ================================================================
# LANGKAH 4: Clone dan Setup Project
# ================================================================
echo ""
echo "[4/7] Menyiapkan project..."

# Buat folder dan clone
if [ -d "$PROJECT_DIR" ]; then
  echo "      Folder $PROJECT_DIR sudah ada, menghapus dan clone ulang..."
  rm -rf "$PROJECT_DIR"
fi

git clone "$REPO_URL" "$PROJECT_DIR"
echo "      Repo berhasil di-clone ke $PROJECT_DIR"

# Buat virtual environment
cd "$PROJECT_DIR"
python${PYTHON_VERSION} -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt
echo "      Dependencies Python berhasil diinstall."

# Buat .env dari .env.example
cp .env.example .env
echo "      File .env berhasil dibuat."

# Perbaiki API_BASE di frontend agar mengarah ke domain
sed -i "s|const API_BASE = 'http://localhost:8000/api/v1';|const API_BASE = 'https://${DOMAIN}/api/v1';|g" frontend/index.html
echo "      Frontend API_BASE diupdate ke https://${DOMAIN}/api/v1"

# Set ownership
chown -R ${APP_USER}:${APP_USER} "$PROJECT_DIR"
echo "      Ownership diset ke user ${APP_USER}."

# Test jalankan (cek apakah bisa start)
echo "      Menguji aplikasi..."
cd "$PROJECT_DIR"
source venv/bin/activate
timeout 5 venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000 &
sleep 3
HEALTH=$(curl -s http://127.0.0.1:8000/health || echo "GAGAL")
kill %1 2>/dev/null || true
wait 2>/dev/null || true

if echo "$HEALTH" | grep -q "Alhamdulillah"; then
  echo "      Tes berhasil: $HEALTH"
else
  echo "      PERINGATAN: Health check tidak merespons seperti yang diharapkan."
  echo "      Response: $HEALTH"
  echo "      Melanjutkan setup... (bisa diperbaiki nanti)"
fi

deactivate

# ================================================================
# LANGKAH 5: Setup Systemd Service
# ================================================================
echo ""
echo "[5/7] Membuat systemd service..."

cat > /etc/systemd/system/tafseer.service << 'SYSTEMD_EOF'
[Unit]
Description=Quran Tafsir API (FastAPI + Uvicorn)
After=network.target

[Service]
User=tafseer
Group=tafseer
WorkingDirectory=/var/www/tafseer
Environment="PATH=/var/www/tafseer/venv/bin:/usr/local/bin:/usr/bin"
EnvironmentFile=/var/www/tafseer/.env
ExecStart=/var/www/tafseer/venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SYSTEMD_EOF

systemctl daemon-reload
systemctl enable tafseer.service
systemctl start tafseer.service

# Tunggu sebentar dan cek status
sleep 3
if systemctl is-active --quiet tafseer.service; then
  echo "      Service tafseer berhasil berjalan."
else
  echo "      PERINGATAN: Service tafseer gagal start."
  echo "      Cek log: sudo journalctl -u tafseer.service -n 20"
fi

# ================================================================
# LANGKAH 6: Setup Nginx Reverse Proxy
# ================================================================
echo ""
echo "[6/7] Mengkonfigurasi Nginx..."

cat > /etc/nginx/sites-available/tafseer << NGINX_EOF
server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAIN} www.${DOMAIN};

    # Batas ukuran upload
    client_max_body_size 10M;

    # Frontend - serve file statis
    location / {
        root ${PROJECT_DIR}/frontend;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API - proxy ke Uvicorn
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 60s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    # API docs
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /redoc {
        proxy_pass http://127.0.0.1:8000/redoc;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /openapi.json {
        proxy_pass http://127.0.0.1:8000/openapi.json;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
NGINX_EOF

# Aktifkan site
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/tafseer /etc/nginx/sites-enabled/tafseer

# Test konfigurasi Nginx
nginx -t
if [ $? -eq 0 ]; then
  systemctl reload nginx
  echo "      Nginx berhasil dikonfigurasi dan di-reload."
else
  echo "      GAGAL: Konfigurasi Nginx tidak valid."
  exit 1
fi

# ================================================================
# LANGKAH 7: Verifikasi
# ================================================================
echo ""
echo "[7/7] Memverifikasi deployment..."
echo ""

# Test health check
echo "--- Health Check (localhost:8000) ---"
curl -s http://127.0.0.1:8000/health | python3 -m json.tool 2>/dev/null || echo "Tidak bisa konek ke backend"

echo ""
echo "--- Health Check via Nginx (localhost:80) ---"
curl -s http://127.0.0.1/health | python3 -m json.tool 2>/dev/null || echo "Tidak bisa konek via Nginx"

echo ""
echo "--- Frontend Check ---"
FRONTEND_CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/)
echo "HTTP Status: $FRONTEND_CHECK"
if [ "$FRONTEND_CHECK" = "200" ]; then
  echo "Frontend berhasil diakses."
else
  echo "PERINGATAN: Frontend mengembalikan status $FRONTEND_CHECK"
fi

# ================================================================
# SELESAI
# ================================================================
echo ""
echo "========================================"
echo "  DEPLOYMENT SELESAI"
echo "========================================"
echo ""
echo "  Status:"
echo "    Backend  : $(systemctl is-active tafseer.service)"
echo "    Nginx    : $(systemctl is-active nginx)"
echo ""
echo "  URL:"
echo "    API      : http://$(hostname -I | awk '{print $1}')/health"
echo "    API Docs : http://$(hostname -I | awk '{print $1}')/docs"
echo "    Frontend : http://$(hostname -I | awk '{print $1}')/"
echo ""
echo "  LANGKAH BERIKUTNYA:"
echo "    1. Arahkan DNS tafseer.my.id -> $(hostname -I | awk '{print $1}')"
echo "    2. Setelah DNS aktif, jalankan:"
echo "       sudo certbot --nginx -d tafseer.my.id"
echo "       (atau gunakan Cloudflare SSL jika pakai proxy Cloudflare)"
echo ""
echo "  PERINTAH BERGUNA:"
echo "    sudo systemctl status tafseer    # Cek status app"
echo "    sudo journalctl -u tafseer -f    # Lihat log app"
echo "    sudo systemctl restart tafseer   # Restart app"
echo "    sudo nginx -t && sudo systemctl reload nginx  # Reload Nginx"
echo ""
