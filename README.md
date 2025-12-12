<p align="center">
  <img src="https://raw.githubusercontent.com/cemal-demirci/proxmox-loadbalancer/master/assets/logo.svg" alt="Proxmox Load Balancer" width="200"/>
</p>

<h1 align="center">🚀 Proxmox Load Balancer</h1>

<p align="center">
  <strong>Proxmox VE cluster'ları için otomatik VM dağıtım ve yük dengeleme aracı</strong>
</p>

<p align="center">
  <a href="#-özellikler">Özellikler</a> •
  <a href="#-kurulum">Kurulum</a> •
  <a href="#-kullanım">Kullanım</a> •
  <a href="#-konfigürasyon">Konfigürasyon</a> •
  <a href="#-sorun-giderme">Sorun Giderme</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Proxmox%20VE-7.x%20%7C%208.x-E57000?style=for-the-badge&logo=proxmox&logoColor=white" alt="Proxmox VE"/>
  <img src="https://img.shields.io/badge/Lisans-MIT-green?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/Shell-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white" alt="Bash"/>
  <img src="https://img.shields.io/badge/Durum-Aktif-success?style=for-the-badge" alt="Status"/>
</p>

---

## 📊 Nasıl Çalışır?

```
                                    🔄 DENGELEME ÖNCESİ
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          ║
    ║   │   NODE 1    │    │   NODE 2    │    │   NODE 3    │          ║
    ║   │   ░░░░░░    │    │   ░░░░░░    │    │   ████████  │          ║
    ║   │    %12      │    │    %14      │    │    %45 ❌   │          ║
    ║   │   5 VM      │    │   5 VM      │    │   20 VM     │          ║
    ║   └─────────────┘    └─────────────┘    └─────────────┘          ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
                                      │
                                      │ 🔄 Script Çalışıyor...
                                      ▼
                                    ✅ DENGELEME SONRASI
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          ║
    ║   │   NODE 1    │    │   NODE 2    │    │   NODE 3    │          ║
    ║   │   ████      │    │   ████      │    │   █████     │          ║
    ║   │    %20      │    │    %22      │    │    %25 ✅   │          ║
    ║   │   8 VM      │    │   8 VM      │    │   14 VM     │          ║
    ║   └─────────────┘    └─────────────┘    └─────────────┘          ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
```

---

## ✨ Özellikler

<table>
<tr>
<td width="50%">

### 🎯 Akıllı Dengeleme
RAM kullanımına göre VM'leri otomatik olarak node'lar arasında dağıtır

### 🔒 HA Entegrasyonu
Proxmox HA Manager ile tam uyumlu çalışır

### 🛡️ VM Koruma
USB passthrough veya özel donanım gerektiren VM'leri hariç tutabilme

</td>
<td width="50%">

### 🧪 Test Modu
Değişiklik yapmadan önce dry-run ile test etme imkanı

### 📝 Detaylı Loglama
Tüm işlemlerin kaydını tutar

### ⏰ Zamanlama
Cron ile otomatik çalıştırma desteği

</td>
</tr>
</table>

---

## 🏗️ Mimari

```
    ┌──────────────────────────────────────────────────────────────────────┐
    │                        PROXMOX CLUSTER                               │
    │                                                                      │
    │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐         │
    │  │     NODE 1     │  │     NODE 2     │  │     NODE 3     │         │
    │  │  ┌──────────┐  │  │  ┌──────────┐  │  │  ┌──────────┐  │         │
    │  │  │ 🖥️ VM-A  │  │  │  │ 🖥️ VM-D  │  │  │  │ 🖥️ VM-G  │  │         │
    │  │  │ 🖥️ VM-B  │  │  │  │ 🖥️ VM-E  │  │  │  │ 🖥️ VM-H  │  │         │
    │  │  │ 🖥️ VM-C  │  │  │  │ 🖥️ VM-F  │  │  │  │ 🖥️ VM-I  │  │         │
    │  │  └──────────┘  │  │  └──────────┘  │  │  │ 🖥️ VM-J  │  │         │
    │  │                │  │                │  │  └──────────┘  │         │
    │  │  RAM: 92GB     │  │  RAM: 105GB    │  │  RAM: 152GB    │         │
    │  │  CPU: 12%      │  │  CPU: 14%      │  │  CPU: 20%      │         │
    │  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘         │
    │          │                   │                   │                  │
    │          └───────────────────┼───────────────────┘                  │
    │                              │                                      │
    │                    ┌─────────▼─────────┐                            │
    │                    │  📦 SHARED STORAGE │                            │
    │                    │   NFS / Ceph / ZFS │                            │
    │                    │      15 TB         │                            │
    │                    └───────────────────┘                            │
    └──────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Gereksinimler

| Gereksinim | Açıklama |
|:----------:|:---------|
| 🖥️ | Proxmox VE 7.x veya 8.x |
| ⚡ | HA Manager aktif |
| 💾 | Shared storage (NFS, Ceph, vb.) |
| 🔑 | Root erişimi |
| 📦 | `jq` paketi (otomatik yüklenir) |

---

## 🚀 Kurulum

### 1️⃣ Repoyu Klonla

```bash
# Proxmox sunucusunda çalıştır
git clone https://github.com/cemal-demirci/proxmox-loadbalancer.git /opt/proxmox-loadbalancer
```

### 2️⃣ Çalıştırılabilir Yap

```bash
chmod +x /opt/proxmox-loadbalancer/proxmox-loadbalancer.sh
```

### 3️⃣ Konfigürasyonu Düzenle

```bash
nano /opt/proxmox-loadbalancer/config.cfg
```

### 4️⃣ Test Et

```bash
# Durum kontrolü
./proxmox-loadbalancer.sh status

# Test modu
./proxmox-loadbalancer.sh dry-run
```

---

## 🎮 Kullanım

```bash
┌─────────────────────────────────────────────────────────────┐
│                     KOMUTLAR                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 ./proxmox-loadbalancer.sh status   → Durum raporu       │
│                                                             │
│  🧪 ./proxmox-loadbalancer.sh dry-run  → Test modu          │
│                                                             │
│  ⚖️  ./proxmox-loadbalancer.sh balance → Dengeleme yap      │
│                                                             │
│  ❓ ./proxmox-loadbalancer.sh help     → Yardım             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 📊 Örnek Çıktı

```
==========================================
CLUSTER DURUM RAPORU
==========================================

NODE KAYNAK KULLANIMI:
----------------------
Node       RAM Kullanım   RAM Toplam      Yüzde     VM Sayısı
--------------------------------------------------------------
VMP2       92GB            754GB           %12        5
VMP3       105GB           754GB           %14        5
VMP4       152GB           754GB           %20        14

VM DAĞILIMI:
------------
✅ service vm:102 (VMP4, started)
✅ service vm:110 (VMP3, started)
✅ service vm:111 (VMP2, started)
...

[INFO] Cluster dengeli durumda (%8 <= %15)
```

---

## ⚙️ Konfigürasyon

### 📁 config.cfg

```bash
# ═══════════════════════════════════════════
# 🖥️ NODE AYARLARI
# ═══════════════════════════════════════════

# Cluster'daki node'lar
NODES="VMP2 VMP3 VMP4"

# Tercih edilen node
PREFERRED_NODE="VMP4"

# ═══════════════════════════════════════════
# ⚖️ DENGELEME AYARLARI
# ═══════════════════════════════════════════

# Dengeleme eşiği (%)
THRESHOLD=15

# Maksimum migration sayısı
MAX_MIGRATIONS=5

# Migration bekleme süresi (saniye)
MIGRATION_WAIT=120

# ═══════════════════════════════════════════
# 🛡️ HARİÇ TUTULAN VM'LER
# ═══════════════════════════════════════════

EXCLUDED_VMS=(
    500     # USB dongle olan VM
)

# ═══════════════════════════════════════════
# 📝 LOG AYARLARI
# ═══════════════════════════════════════════

LOG_FILE="/var/log/proxmox-loadbalancer.log"
LOG_LEVEL="INFO"
```

### 📊 Parametre Referansı

<table>
<tr>
<th>Parametre</th>
<th>Açıklama</th>
<th>Varsayılan</th>
</tr>
<tr>
<td><code>NODES</code></td>
<td>Cluster node'ları (boşlukla ayrılmış)</td>
<td><code>"node1 node2 node3"</code></td>
</tr>
<tr>
<td><code>THRESHOLD</code></td>
<td>Dengeleme eşiği (%)</td>
<td><code>15</code></td>
</tr>
<tr>
<td><code>MAX_MIGRATIONS</code></td>
<td>Tek çalışmada maksimum migration</td>
<td><code>5</code></td>
</tr>
<tr>
<td><code>MIGRATION_WAIT</code></td>
<td>Migration bekleme süresi (saniye)</td>
<td><code>120</code></td>
</tr>
<tr>
<td><code>EXCLUDED_VMS</code></td>
<td>Taşınmayacak VM ID'leri</td>
<td><code>()</code></td>
</tr>
</table>

---

## ⏰ Otomatik Zamanlama

```bash
# Her 6 saatte bir çalıştır
echo "0 */6 * * * /opt/proxmox-loadbalancer/proxmox-loadbalancer.sh balance" | crontab -

# Veya her gece 02:00'de
echo "0 2 * * * /opt/proxmox-loadbalancer/proxmox-loadbalancer.sh balance" | crontab -
```

---

## 🔄 Çalışma Prensibi

```
    ┌─────────────────────────────────────────────────────────────┐
    │                    🔄 DENGELEME DÖNGÜSÜ                     │
    └─────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  1️⃣ Node Yüklerini Al  │
                    │    (RAM Kullanımı)     │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │  2️⃣ Fark Hesapla       │
                    │  (Max - Min Yük)       │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │  3️⃣ Eşik Kontrolü      │◄──────┐
                    │  Fark > %15 ?          │       │
                    └───────────┬────────────┘       │
                          │           │              │
                     EVET │           │ HAYIR        │
                          ▼           ▼              │
            ┌──────────────────┐  ┌──────────┐      │
            │ 4️⃣ En Büyük VM'i │  │ ✅ Bitti │      │
            │    Seç & Taşı    │  └──────────┘      │
            └────────┬─────────┘                    │
                     │                              │
                     ▼                              │
            ┌──────────────────┐                    │
            │ 5️⃣ Bekle (120s)  │────────────────────┘
            └──────────────────┘
```

---

## 🔧 Sorun Giderme

<details>
<summary><b>❌ Migration Başarısız Oluyor</b></summary>

```bash
# 1. NFS Mount Kontrolü
mount | grep nfs-storage

# 2. HA Durumu Kontrolü
ha-manager status

# 3. Log Kontrolü
tail -f /var/log/proxmox-loadbalancer.log
journalctl -u pve-ha-lrm -f
```

</details>

<details>
<summary><b>❌ Node Erişilemiyor</b></summary>

```bash
# Node bağlantısını test et
ping VMP2
ssh root@VMP2 hostname
```

</details>

<details>
<summary><b>❌ VM Taşınamıyor</b></summary>

- 🔌 USB passthrough varsa → `EXCLUDED_VMS`'e ekle
- 💾 Local disk varsa → Shared storage'a taşı
- 🔒 HA grubu kısıtlamalarını kontrol et

</details>

---

## 📈 Performans İpuçları

| İpucu | Açıklama |
|:-----:|:---------|
| 🎯 | `THRESHOLD` değerini ortamınıza göre ayarlayın |
| ⏱️ | Yoğun saatlerde cron çalıştırmaktan kaçının |
| 📊 | Düzenli olarak logları kontrol edin |
| 🛡️ | Kritik VM'leri `EXCLUDED_VMS`'e ekleyin |

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull Request göndermekten çekinmeyin.

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

## 📜 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 👨‍💻 Yazar

<p align="center">
  <strong>Cemal Demirci</strong><br>
  <a href="https://github.com/cemal-demirci">GitHub</a>
</p>

---

<p align="center">
  <sub>Proxmox topluluğu için ❤️ ile yapıldı</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/cemal-demirci/proxmox-loadbalancer?style=social" alt="Stars"/>
  <img src="https://img.shields.io/github/forks/cemal-demirci/proxmox-loadbalancer?style=social" alt="Forks"/>
</p>
