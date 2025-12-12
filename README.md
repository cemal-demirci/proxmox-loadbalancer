<p align="center">
  <img src="https://raw.githubusercontent.com/cemal-demirci/proxmox-loadbalancer/master/assets/logo.svg" alt="Proxmox Load Balancer" width="200"/>
</p>

<h1 align="center">🚀 Proxmox Load Balancer</h1>

<p align="center">
  <strong>Proxmox VE cluster'ları için gelişmiş otomatik VM dağıtım ve yük dengeleme aracı</strong>
</p>

<p align="center">
  <a href="#-özellikler">Özellikler</a> •
  <a href="#-kurulum">Kurulum</a> •
  <a href="#-kullanım">Kullanım</a> •
  <a href="#-konfigürasyon">Konfigürasyon</a> •
  <a href="#-gelişmiş-özellikler">Gelişmiş</a> •
  <a href="#-sorun-giderme">Sorun Giderme</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Proxmox%20VE-7.x%20%7C%208.x-E57000?style=for-the-badge&logo=proxmox&logoColor=white" alt="Proxmox VE"/>
  <img src="https://img.shields.io/badge/Lisans-MIT-green?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/Shell-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white" alt="Bash"/>
  <img src="https://img.shields.io/badge/Versiyon-2.0-blue?style=for-the-badge" alt="Version"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/cemal-demirci/proxmox-loadbalancer?style=social" alt="Stars"/>
  <img src="https://img.shields.io/github/forks/cemal-demirci/proxmox-loadbalancer?style=social" alt="Forks"/>
  <img src="https://img.shields.io/github/watchers/cemal-demirci/proxmox-loadbalancer?style=social" alt="Watchers"/>
</p>

---

## 📊 Nasıl Çalışır?

```
                                    🔄 DENGELEME ÖNCESİ
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐            ║
    ║   │    NODE 1     │    │    NODE 2     │    │    NODE 3     │            ║
    ║   │   ░░░░░░░░    │    │   ░░░░░░░░    │    │   ██████████  │            ║
    ║   │    RAM: %12   │    │    RAM: %14   │    │    RAM: %45   │            ║
    ║   │    CPU: %8    │    │    CPU: %12   │    │    CPU: %65   │            ║
    ║   │    5 VM       │    │    5 VM       │    │    20 VM  ⚠️  │            ║
    ║   └───────────────┘    └───────────────┘    └───────────────┘            ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
                                        │
                                        │ 🔄 Akıllı Algoritma Çalışıyor...
                                        │ 📊 Kaynak analizi yapılıyor
                                        │ 🎯 Optimal dağılım hesaplanıyor
                                        ▼
                                    ✅ DENGELEME SONRASI
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐            ║
    ║   │    NODE 1     │    │    NODE 2     │    │    NODE 3     │            ║
    ║   │   ██████      │    │   ██████      │    │   ███████     │            ║
    ║   │    RAM: %22   │    │    RAM: %24   │    │    RAM: %26   │            ║
    ║   │    CPU: %20   │    │    CPU: %22   │    │    CPU: %25   │            ║
    ║   │    10 VM  ✅  │    │    10 VM  ✅  │    │    10 VM  ✅  │            ║
    ║   └───────────────┘    └───────────────┘    └───────────────┘            ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## ✨ Özellikler

<table>
<tr>
<td width="33%">

### 🎯 Akıllı Dengeleme
- RAM bazlı dengeleme
- CPU bazlı dengeleme
- Hibrit mod desteği
- Ağırlıklı skorlama

</td>
<td width="33%">

### 🔒 Güvenlik & HA
- Proxmox HA entegrasyonu
- Güvenli migration
- Rollback desteği
- Cluster durumu izleme

</td>
<td width="33%">

### 🛡️ VM Koruma
- USB passthrough koruması
- Local disk tespiti
- HA grup kısıtlamaları
- Kritik VM listesi

</td>
</tr>
<tr>
<td width="33%">

### 📊 İzleme & Raporlama
- Gerçek zamanlı durum
- Renkli terminal çıktısı
- Detaylı loglar
- Tarihsel veriler

</td>
<td width="33%">

### ⚡ Performans
- Paralel işlem desteği
- Hızlı kaynak sorguları
- Optimize edilmiş JSON parsing
- Düşük sistem yükü

</td>
<td width="33%">

### 🔧 Esneklik
- Kolay konfigürasyon
- Cron zamanlama
- Dry-run modu
- Verbose çıktı

</td>
</tr>
</table>

---

## 🆕 Versiyon 2.0 Yenilikleri

| Özellik | Açıklama |
|:-------:|:---------|
| 🎨 | **Renkli Terminal Çıktısı** - Kolay okunabilir formatlanmış çıktı |
| 📈 | **CPU Dengeleme** - Sadece RAM değil, CPU bazlı dengeleme |
| 🔄 | **Hibrit Mod** - RAM + CPU kombinasyonlu akıllı dengeleme |
| 📊 | **Gelişmiş Raporlama** - Detaylı cluster analizi |
| 🔔 | **Bildirim Desteği** - Webhook ve email entegrasyonu |
| 🛡️ | **Güvenlik Kontrolleri** - Migration öncesi doğrulama |
| 📝 | **JSON Çıktı** - Otomasyon için makine okunabilir format |
| ⏱️ | **Zamanlama** - Gelişmiş cron ifadeleri desteği |

---

## 🏗️ Mimari

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PROXMOX CLUSTER                                    │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        🔄 LOAD BALANCER ENGINE                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │   │
│  │  │  Collector  │  │  Analyzer   │  │  Scheduler  │  │  Migrator   │    │   │
│  │  │  📊 Metrics │──│  🧮 Score   │──│  📋 Plan    │──│  🚀 Execute │    │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                       │                                         │
│         ┌─────────────────────────────┼─────────────────────────────┐          │
│         │                             │                             │          │
│         ▼                             ▼                             ▼          │
│  ┌────────────────┐           ┌────────────────┐           ┌────────────────┐  │
│  │     NODE 1     │           │     NODE 2     │           │     NODE 3     │  │
│  │ ═══════════════│           │ ═══════════════│           │ ═══════════════│  │
│  │ 🖥️ VM-101      │           │ 🖥️ VM-201      │           │ 🖥️ VM-301      │  │
│  │ 🖥️ VM-102      │           │ 🖥️ VM-202      │           │ 🖥️ VM-302      │  │
│  │ 🖥️ VM-103      │           │ 🖥️ VM-203      │           │ 🖥️ VM-303      │  │
│  │ ───────────────│           │ ───────────────│           │ 🖥️ VM-304      │  │
│  │ 💾 RAM: 92GB   │           │ 💾 RAM: 105GB  │           │ ───────────────│  │
│  │ ⚡ CPU: 12%    │           │ ⚡ CPU: 14%    │           │ 💾 RAM: 152GB  │  │
│  │ 📦 VMs: 5      │           │ 📦 VMs: 5      │           │ ⚡ CPU: 20%    │  │
│  └───────┬────────┘           └───────┬────────┘           │ 📦 VMs: 14     │  │
│          │                            │                    └───────┬────────┘  │
│          │                            │                            │           │
│          └────────────────────────────┼────────────────────────────┘           │
│                                       │                                         │
│                          ┌────────────▼────────────┐                           │
│                          │    📦 SHARED STORAGE    │                           │
│                          │  ┌──────────────────┐   │                           │
│                          │  │ 🗄️ NFS / Ceph    │   │                           │
│                          │  │ 💽 ZFS / GlusterFS│   │                           │
│                          │  │ 📊 15 TB Kapasite │   │                           │
│                          │  └──────────────────┘   │                           │
│                          └─────────────────────────┘                           │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Gereksinimler

| Gereksinim | Minimum | Önerilen |
|:----------:|:-------:|:--------:|
| 🖥️ **Proxmox VE** | 7.0 | 8.x |
| 💾 **RAM** | 512MB | 1GB+ |
| ⚡ **CPU** | 1 Core | 2+ Core |
| 📦 **Paketler** | bash, jq | + curl, mail |
| 🔒 **Erişim** | Root | Root |
| 💽 **Storage** | Shared | NFS/Ceph |

---

## 🚀 Kurulum

### 📥 Otomatik Kurulum (Önerilen)

```bash
# Tek komutla kurulum
curl -sSL https://raw.githubusercontent.com/cemal-demirci/proxmox-loadbalancer/master/install.sh | bash
```

### 📦 Manuel Kurulum

#### 1️⃣ Repoyu Klonla

```bash
# Proxmox sunucusunda çalıştır
git clone https://github.com/cemal-demirci/proxmox-loadbalancer.git /opt/proxmox-loadbalancer
cd /opt/proxmox-loadbalancer
```

#### 2️⃣ Bağımlılıkları Yükle

```bash
# Gerekli paketleri yükle
apt-get update && apt-get install -y jq curl
```

#### 3️⃣ Çalıştırılabilir Yap

```bash
chmod +x /opt/proxmox-loadbalancer/*.sh
```

#### 4️⃣ Konfigürasyonu Düzenle

```bash
# Konfigürasyon dosyasını düzenle
cp config.cfg.example config.cfg
nano config.cfg
```

#### 5️⃣ Test Et

```bash
# Durum kontrolü
./proxmox-loadbalancer.sh status

# Test modu (değişiklik yapmaz)
./proxmox-loadbalancer.sh dry-run
```

---

## 🎮 Kullanım

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              📋 KOMUTLAR                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📊 ./proxmox-loadbalancer.sh status      →  Cluster durum raporu          │
│  🧪 ./proxmox-loadbalancer.sh dry-run     →  Test modu (değişiklik yok)    │
│  ⚖️  ./proxmox-loadbalancer.sh balance    →  Yük dengeleme başlat          │
│  📈 ./proxmox-loadbalancer.sh analyze     →  Detaylı cluster analizi       │
│  📝 ./proxmox-loadbalancer.sh history     →  Migration geçmişi             │
│  🔧 ./proxmox-loadbalancer.sh config      →  Konfigürasyon göster          │
│  ❓ ./proxmox-loadbalancer.sh help        →  Yardım mesajı                 │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                              🎛️ SEÇENEKLER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  --verbose, -v     →  Detaylı çıktı                                        │
│  --quiet, -q       →  Sessiz mod                                           │
│  --json            →  JSON formatında çıktı                                │
│  --no-color        →  Renksiz çıktı                                        │
│  --force           →  Onay istemeden çalıştır                              │
│  --max-migrations  →  Maksimum migration sayısı                            │
│  --threshold       →  Dengeleme eşiği (%)                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📊 Örnek Çıktılar

#### Status Komutu
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🖥️  PROXMOX CLUSTER DURUMU                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Cluster: production-cluster    Nodes: 3    Total VMs: 24    HA: ✅ Active  ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────┐
│                            📊 NODE KAYNAK KULLANIMI                          │
├──────────┬───────────────┬───────────────┬──────────┬──────────┬─────────────┤
│   Node   │  RAM Kullanım │  RAM Toplam   │   RAM %  │   CPU %  │   VM Sayısı │
├──────────┼───────────────┼───────────────┼──────────┼──────────┼─────────────┤
│   VMP2   │     92 GB     │    754 GB     │   ██░░ 12%   │   █░░░  8%  │      5      │
│   VMP3   │    105 GB     │    754 GB     │   ██░░ 14%   │   █░░░ 12%  │      5      │
│   VMP4   │    152 GB     │    754 GB     │   ███░ 20%   │   ██░░ 18%  │     14      │
└──────────┴───────────────┴───────────────┴──────────┴──────────┴─────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                              📈 DENGE ANALİZİ                                │
├──────────────────────────────────────────────────────────────────────────────┤
│  RAM Farkı: 8%  (Max: 20% - Min: 12%)     Eşik: 15%    Durum: ✅ DENGELİ    │
│  CPU Farkı: 10% (Max: 18% - Min: 8%)      Eşik: 30%    Durum: ✅ DENGELİ    │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                              🖥️ VM DAĞILIMI                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│  ✅ vm:102  │ VMP4 │ started │ 8GB  RAM │ 4 CPU │ web-server              │
│  ✅ vm:110  │ VMP3 │ started │ 16GB RAM │ 8 CPU │ database                │
│  ✅ vm:111  │ VMP2 │ started │ 4GB  RAM │ 2 CPU │ monitoring              │
│  🔒 vm:500  │ VMP3 │ started │ 32GB RAM │ 8 CPU │ OLYMPOS [USB Protected] │
│  ...                                                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### Analyze Komutu
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          📊 DETAYLI CLUSTER ANALİZİ                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

📈 KAYNAK DAĞILIMI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  VMP2  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  12% RAM
  VMP3  ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  14% RAM
  VMP4  ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  20% RAM

📊 İSTATİSTİKLER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Toplam RAM       : 2,262 GB
  • Kullanılan RAM   : 349 GB (15.4%)
  • Toplam VM        : 24
  • Ortalama VM/Node : 8
  • En Yüklü Node    : VMP4 (20%)
  • En Boş Node      : VMP2 (12%)
  • Denge Skoru      : 92/100 ⭐⭐⭐⭐⭐

🎯 ÖNERİLER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Cluster iyi dengelenmiş durumda
  💡 Yük farkı eşik değerinin altında (%8 < %15)
  📝 Bir sonraki kontrol: 6 saat sonra
```

---

## ⚙️ Konfigürasyon

### 📁 config.cfg

```bash
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                    PROXMOX LOAD BALANCER v2.0                             ║
# ║                       Konfigürasyon Dosyası                               ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

# ═══════════════════════════════════════════
# 🖥️ CLUSTER AYARLARI
# ═══════════════════════════════════════════

# Cluster'daki node'lar (boşlukla ayrılmış)
NODES="VMP2 VMP3 VMP4"

# Tercih edilen node (yeni VM'ler için)
PREFERRED_NODE="VMP4"

# Cluster adı (raporlama için)
CLUSTER_NAME="production-cluster"

# ═══════════════════════════════════════════
# ⚖️ DENGELEME AYARLARI
# ═══════════════════════════════════════════

# Dengeleme modu: ram, cpu, hybrid
BALANCE_MODE="ram"

# RAM dengeleme eşiği (%)
RAM_THRESHOLD=15

# CPU dengeleme eşiği (%)
CPU_THRESHOLD=30

# Hibrit mod ağırlıkları (toplam 100 olmalı)
RAM_WEIGHT=70
CPU_WEIGHT=30

# Maksimum migration sayısı (tek çalışmada)
MAX_MIGRATIONS=5

# Migration bekleme süresi (saniye)
MIGRATION_WAIT=120

# Paralel migration (true/false)
PARALLEL_MIGRATION=false

# ═══════════════════════════════════════════
# 🛡️ VM KORUMA AYARLARI
# ═══════════════════════════════════════════

# Taşınmayacak VM'ler (VMID listesi)
EXCLUDED_VMS=(
    500     # OLYMPOS - USB CodeMeter dongle
    # 100   # Kritik sistem VM'i
)

# Minimum VM boyutu (taşıma için, bytes)
MIN_VM_SIZE=1073741824  # 1GB

# Local disk olan VM'leri atla
SKIP_LOCAL_DISK=true

# HA grubuna göre kısıtla
RESPECT_HA_GROUPS=true

# ═══════════════════════════════════════════
# 📝 LOG AYARLARI
# ═══════════════════════════════════════════

# Log dosyası yolu
LOG_FILE="/var/log/proxmox-loadbalancer.log"

# Log seviyesi: DEBUG, INFO, WARN, ERROR
LOG_LEVEL="INFO"

# Log rotasyonu (gün)
LOG_RETENTION=30

# Renkli log çıktısı
COLOR_OUTPUT=true

# ═══════════════════════════════════════════
# 🔔 BİLDİRİM AYARLARI
# ═══════════════════════════════════════════

# Email bildirimi
EMAIL_ENABLED=false
EMAIL_TO="admin@example.com"
EMAIL_SUBJECT_PREFIX="[Proxmox-LB]"

# Webhook bildirimi (Slack, Discord, Teams, vb.)
WEBHOOK_ENABLED=false
WEBHOOK_URL=""

# Bildirim gönderme durumları
NOTIFY_ON_MIGRATION=true
NOTIFY_ON_ERROR=true
NOTIFY_ON_BALANCE=false

# ═══════════════════════════════════════════
# ⏰ ZAMANLAMA AYARLARI
# ═══════════════════════════════════════════

# Otomatik çalışma saatleri (7/24 için boş bırak)
ALLOWED_HOURS=""  # Örnek: "02:00-06:00"

# Hafta sonu çalışma
RUN_ON_WEEKENDS=true

# Bakım modu (true ise script çalışmaz)
MAINTENANCE_MODE=false
```

### 📊 Parametre Referansı

<details>
<summary><b>🖥️ Cluster Ayarları</b></summary>

| Parametre | Açıklama | Varsayılan | Örnek |
|:---------:|:---------|:-----------|:------|
| `NODES` | Cluster node listesi | - | `"VMP2 VMP3 VMP4"` |
| `PREFERRED_NODE` | Tercih edilen node | - | `"VMP4"` |
| `CLUSTER_NAME` | Cluster adı | `"cluster"` | `"production"` |

</details>

<details>
<summary><b>⚖️ Dengeleme Ayarları</b></summary>

| Parametre | Açıklama | Varsayılan | Aralık |
|:---------:|:---------|:-----------|:-------|
| `BALANCE_MODE` | Dengeleme modu | `"ram"` | ram/cpu/hybrid |
| `RAM_THRESHOLD` | RAM eşiği | `15` | 5-50% |
| `CPU_THRESHOLD` | CPU eşiği | `30` | 10-70% |
| `RAM_WEIGHT` | RAM ağırlığı | `70` | 0-100 |
| `CPU_WEIGHT` | CPU ağırlığı | `30` | 0-100 |
| `MAX_MIGRATIONS` | Max migration | `5` | 1-20 |
| `MIGRATION_WAIT` | Bekleme süresi | `120` | 30-600s |

</details>

<details>
<summary><b>🛡️ VM Koruma</b></summary>

| Parametre | Açıklama | Varsayılan |
|:---------:|:---------|:-----------|
| `EXCLUDED_VMS` | Hariç tutulan VM'ler | `()` |
| `MIN_VM_SIZE` | Minimum VM boyutu | `1GB` |
| `SKIP_LOCAL_DISK` | Local disk atla | `true` |
| `RESPECT_HA_GROUPS` | HA gruplarına uy | `true` |

</details>

---

## 🔄 Çalışma Prensibi

```
    ┌─────────────────────────────────────────────────────────────────┐
    │                    🔄 DENGELEME ALGORİTMASI v2.0                │
    └─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  1️⃣  VERİ TOPLAMA             │
                    │  ├─ Node kaynak bilgileri     │
                    │  ├─ VM listesi ve durumları   │
                    │  └─ HA grup konfigürasyonu    │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  2️⃣  SKOR HESAPLAMA           │
                    │  ├─ RAM kullanım skoru        │
                    │  ├─ CPU kullanım skoru        │
                    │  └─ Hibrit skor (ağırlıklı)   │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  3️⃣  ANALİZ                   │
                    │  ├─ En yüklü node belirleme   │
                    │  ├─ En boş node belirleme     │
                    │  └─ Fark hesaplama            │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  4️⃣  EŞİK KONTROLÜ            │◄──────────────┐
                    │  Fark > Threshold ?           │               │
                    └───────────────┬───────────────┘               │
                              │           │                         │
                         EVET │           │ HAYIR                   │
                              ▼           ▼                         │
            ┌─────────────────────┐  ┌──────────────┐              │
            │ 5️⃣  VM SEÇİMİ       │  │  ✅ TAMAMLANDI│              │
            │ ├─ Excluded kontrol │  │  Cluster     │              │
            │ ├─ Local disk kontrol│  │  dengeli!    │              │
            │ ├─ HA grup kontrol  │  └──────────────┘              │
            │ └─ Boyut sıralaması │                                │
            └──────────┬──────────┘                                │
                       │                                           │
                       ▼                                           │
            ┌─────────────────────┐                                │
            │ 6️⃣  GÜVENLİK KONTROL│                                │
            │ ├─ Storage erişimi  │                                │
            │ ├─ Network durumu   │                                │
            │ └─ HA status        │                                │
            └──────────┬──────────┘                                │
                       │                                           │
                       ▼                                           │
            ┌─────────────────────┐                                │
            │ 7️⃣  MİGRASYON       │                                │
            │ ├─ HA migrate komutu│                                │
            │ ├─ İlerleme izleme  │                                │
            │ └─ Sonuç doğrulama  │                                │
            └──────────┬──────────┘                                │
                       │                                           │
                       ▼                                           │
            ┌─────────────────────┐                                │
            │ 8️⃣  BEKLEME & LOG   │                                │
            │ ├─ Migration bekle  │                                │
            │ ├─ Log kaydı        │                                │
            │ └─ Bildirim gönder  │────────────────────────────────┘
            └─────────────────────┘
```

---

## 🔧 Gelişmiş Özellikler

### 🎨 Renkli Terminal Çıktısı

Script, terminal çıktılarında renk kodları kullanarak okunabilirliği artırır:

| Renk | Anlam |
|:----:|:------|
| 🟢 Yeşil | Başarılı işlem, dengeli durum |
| 🟡 Sarı | Uyarı, dikkat gerektiren durum |
| 🔴 Kırmızı | Hata, kritik durum |
| 🔵 Mavi | Bilgi, neutral mesaj |
| ⚪ Beyaz | Normal çıktı |

### 📊 JSON Çıktı Modu

Otomasyon ve entegrasyon için JSON formatında çıktı:

```bash
./proxmox-loadbalancer.sh status --json
```

```json
{
  "cluster": {
    "name": "production-cluster",
    "nodes": 3,
    "total_vms": 24,
    "ha_status": "active"
  },
  "nodes": [
    {
      "name": "VMP2",
      "ram_used_gb": 92,
      "ram_total_gb": 754,
      "ram_percent": 12,
      "cpu_percent": 8,
      "vm_count": 5
    }
  ],
  "balance": {
    "ram_diff": 8,
    "cpu_diff": 10,
    "status": "balanced"
  }
}
```

### 🔔 Bildirim Entegrasyonu

#### Slack Webhook
```bash
WEBHOOK_ENABLED=true
WEBHOOK_URL="https://hooks.slack.com/services/xxx/yyy/zzz"
```

#### Discord Webhook
```bash
WEBHOOK_URL="https://discord.com/api/webhooks/xxx/yyy"
```

#### Email
```bash
EMAIL_ENABLED=true
EMAIL_TO="admin@example.com"
```

---

## ⏰ Otomatik Zamanlama

### Cron Örnekleri

```bash
# Her 6 saatte bir
0 */6 * * * /opt/proxmox-loadbalancer/proxmox-loadbalancer.sh balance --quiet

# Her gece 02:00'de
0 2 * * * /opt/proxmox-loadbalancer/proxmox-loadbalancer.sh balance

# Hafta içi her gün 03:00'de
0 3 * * 1-5 /opt/proxmox-loadbalancer/proxmox-loadbalancer.sh balance

# Her Pazar 04:00'de detaylı analiz
0 4 * * 0 /opt/proxmox-loadbalancer/proxmox-loadbalancer.sh analyze --json > /var/log/weekly-analysis.json
```

### Systemd Timer (Alternatif)

```ini
# /etc/systemd/system/proxmox-loadbalancer.timer
[Unit]
Description=Proxmox Load Balancer Timer

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

---

## 🔧 Sorun Giderme

<details>
<summary><b>❌ Migration Başarısız Oluyor</b></summary>

### Olası Sebepler ve Çözümler

**1. NFS Mount Sorunu**
```bash
# Tüm node'larda kontrol et
for node in VMP2 VMP3 VMP4; do
  echo "=== $node ==="
  ssh root@$node "mount | grep nfs-storage"
done

# Mount yoksa ekle
mount -t nfs 172.16.0.66:/mnt/nfs-storage /mnt/nfs-storage
```

**2. HA Durumu**
```bash
# HA status kontrol
ha-manager status

# Fence durumu
pvecm status
```

**3. Network Sorunu**
```bash
# Node'lar arası bağlantı
ping -c 3 VMP2
ping -c 3 VMP3
```

</details>

<details>
<summary><b>❌ Script Çalışmıyor</b></summary>

**1. İzin Kontrolü**
```bash
ls -la /opt/proxmox-loadbalancer/
chmod +x /opt/proxmox-loadbalancer/*.sh
```

**2. Bağımlılık Kontrolü**
```bash
which jq || apt-get install -y jq
which curl || apt-get install -y curl
```

**3. Config Kontrolü**
```bash
./proxmox-loadbalancer.sh config
```

</details>

<details>
<summary><b>❌ VM Taşınamıyor</b></summary>

| Sebep | Çözüm |
|:------|:------|
| USB Passthrough | `EXCLUDED_VMS`'e ekle |
| Local Disk | Shared storage'a taşı |
| HA Grup Kısıtı | HA grubunu düzenle |
| Yetersiz RAM | Hedef node'da yer aç |

</details>

---

## 📈 Performans İpuçları

| İpucu | Açıklama |
|:-----:|:---------|
| 🎯 | `THRESHOLD` değerini ortamınıza göre ayarlayın (genelde %10-20) |
| ⏱️ | Yoğun saatlerde çalıştırmaktan kaçının (`ALLOWED_HOURS` kullanın) |
| 📊 | Düzenli olarak logları kontrol edin |
| 🛡️ | Kritik VM'leri mutlaka `EXCLUDED_VMS`'e ekleyin |
| 🔄 | Hibrit mod kullanarak daha dengeli dağılım sağlayın |
| 📦 | Küçük VM'leri taşımak için `MIN_VM_SIZE` değerini düşürün |

---

## 🗺️ Yol Haritası

- [x] v1.0 - Temel RAM dengeleme
- [x] v2.0 - CPU dengeleme, renkli çıktı
- [ ] v2.1 - Web arayüzü (Proxmox entegre)
- [ ] v2.2 - Prometheus metrikleri
- [ ] v3.0 - ML tabanlı tahminleme

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull Request göndermekten çekinmeyin.

```bash
# 1. Fork edin
# 2. Feature branch oluşturun
git checkout -b feature/amazing-feature

# 3. Değişikliklerinizi commit edin
git commit -m 'Add amazing feature'

# 4. Branch'inizi push edin
git push origin feature/amazing-feature

# 5. Pull Request açın
```

---

## 📜 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 👨‍💻 Yazarlar

<p align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/cemal-demirci">
          <img src="https://github.com/cemal-demirci.png" width="100px;" alt="Cemal Demirci"/><br />
          <sub><b>Cemal Demirci</b></sub>
        </a><br />
        <sub>💻 Geliştirici</sub>
      </td>
      <td align="center">
        <a href="https://github.com/muammer-yesilyagci">
          <img src="https://github.com/muammer-yesilyagci.png" width="100px;" alt="Muammer Yeşilyağcı"/><br />
          <sub><b>Muammer Yeşilyağcı</b></sub>
        </a><br />
        <sub>🏗️ Mimar & Geliştirici</sub>
      </td>
    </tr>
  </table>
</p>

---

## 🙏 Teşekkürler

- [Proxmox VE](https://www.proxmox.com/) - Harika sanallaştırma platformu
- [jq](https://stedolan.github.io/jq/) - JSON işleme aracı
- Tüm katkıda bulunanlara teşekkürler!

---

<p align="center">
  <sub>Proxmox topluluğu için ❤️ ile yapıldı</sub>
</p>

<p align="center">
  <a href="https://github.com/cemal-demirci/proxmox-loadbalancer/stargazers">
    <img src="https://img.shields.io/github/stars/cemal-demirci/proxmox-loadbalancer?style=for-the-badge&logo=github&color=yellow" alt="Stars"/>
  </a>
  <a href="https://github.com/cemal-demirci/proxmox-loadbalancer/network/members">
    <img src="https://img.shields.io/github/forks/cemal-demirci/proxmox-loadbalancer?style=for-the-badge&logo=github&color=blue" alt="Forks"/>
  </a>
  <a href="https://github.com/cemal-demirci/proxmox-loadbalancer/issues">
    <img src="https://img.shields.io/github/issues/cemal-demirci/proxmox-loadbalancer?style=for-the-badge&logo=github&color=red" alt="Issues"/>
  </a>
</p>

<p align="center">
  <sub>© 2025 Cemal Demirci & Muammer Yeşilyağcı. Tüm hakları saklıdır.</sub>
</p>
