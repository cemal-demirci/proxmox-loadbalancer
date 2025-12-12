# Proxmox Load Balancer - Hızlı Kurulum

## Tek Komutla Kurulum

Proxmox sunucusunda (herhangi bir node'da) çalıştır:

```bash
# 1. Klasör oluştur
mkdir -p /opt/proxmox-loadbalancer

# 2. Bu klasördeki tüm dosyaları kopyala
# (SCP veya manuel)

# 3. Çalıştırılabilir yap
chmod +x /opt/proxmox-loadbalancer/proxmox-loadbalancer.sh

# 4. Test et
/opt/proxmox-loadbalancer/proxmox-loadbalancer.sh status
```

## SCP ile Kopyalama

Windows'tan Proxmox'a:

```powershell
scp -r "C:\Users\cemal.demirci\Desktop\Proxmox-Loadbalancer\*" root@172.16.0.65:/opt/proxmox-loadbalancer/
```

## Hızlı Konfigürasyon

`config.cfg` dosyasında sadece şunları değiştir:

```bash
# Node'larınızı tanımlayın
NODES="VMP2 VMP3 VMP4"

# Taşınmaması gereken VM'ler
EXCLUDED_VMS=(
    500     # USB dongle olan VM
)
```

## Otomatik Çalıştırma (Cron)

```bash
# Crontab'a ekle
echo "0 */6 * * * /opt/proxmox-loadbalancer/proxmox-loadbalancer.sh balance" | crontab -
```

## Komutlar

| Komut | Açıklama |
|-------|----------|
| `./proxmox-loadbalancer.sh status` | Durum göster |
| `./proxmox-loadbalancer.sh dry-run` | Test modu |
| `./proxmox-loadbalancer.sh balance` | Dengeleme yap |

## Kontrol

```bash
# Çalıştıktan sonra
tail -f /var/log/proxmox-loadbalancer.log
```
