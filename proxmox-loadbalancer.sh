#!/bin/bash
#
# Proxmox Load Balancer
# Otomatik VM dagitim ve load balancing scripti
#
# Author: Zero Density IT
# Version: 1.0
# Date: 2025-12-12
#

set -e

# Konfigürasyon dosyasını yükle
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config.cfg"

if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
else
    echo "HATA: config.cfg bulunamadi!"
    exit 1
fi

# Log fonksiyonu
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Node kaynak bilgilerini al
get_node_resources() {
    pvesh get /cluster/resources --type node --output-format json 2>/dev/null
}

# VM listesini al
get_vm_list() {
    pvesh get /cluster/resources --type vm --output-format json 2>/dev/null
}

# Node RAM kullanım yüzdesini hesapla
get_node_mem_percent() {
    local node="$1"
    local json=$(get_node_resources)
    local mem=$(echo "$json" | jq -r ".[] | select(.node==\"$node\") | .mem")
    local maxmem=$(echo "$json" | jq -r ".[] | select(.node==\"$node\") | .maxmem")

    if [[ -n "$mem" && -n "$maxmem" && "$maxmem" -gt 0 ]]; then
        echo $((mem * 100 / maxmem))
    else
        echo "0"
    fi
}

# Node'daki VM sayısını al
get_node_vm_count() {
    local node="$1"
    ha-manager status 2>/dev/null | grep -c "$node, started" || echo "0"
}

# En az yüklü node'u bul
find_least_loaded_node() {
    local min_load=100
    local best_node=""

    for node in $NODES; do
        local load=$(get_node_mem_percent "$node")
        if [[ "$load" -lt "$min_load" ]]; then
            min_load=$load
            best_node=$node
        fi
    done

    echo "$best_node"
}

# En çok yüklü node'u bul
find_most_loaded_node() {
    local max_load=0
    local worst_node=""

    for node in $NODES; do
        local load=$(get_node_mem_percent "$node")
        if [[ "$load" -gt "$max_load" ]]; then
            max_load=$load
            worst_node=$node
        fi
    done

    echo "$worst_node"
}

# VM'i migrate et
migrate_vm() {
    local vmid="$1"
    local target_node="$2"

    log "INFO" "VM $vmid -> $target_node migrate ediliyor..."

    if ha-manager migrate "vm:$vmid" "$target_node" 2>/dev/null; then
        log "INFO" "VM $vmid migrate komutu gönderildi"
        return 0
    else
        log "ERROR" "VM $vmid migrate edilemedi"
        return 1
    fi
}

# Node'daki en büyük VM'i bul (RAM bazlı)
find_largest_vm_on_node() {
    local node="$1"
    local json=$(get_vm_list)

    # Excluded VM'leri filtrele
    local largest_vmid=""
    local largest_mem=0

    # jq ile VM listesini parse et
    while IFS="|" read -r vmid maxmem vm_node; do
        # Excluded VM'leri atla
        if [[ " ${EXCLUDED_VMS[*]} " =~ " $vmid " ]]; then
            continue
        fi

        if [[ "$vm_node" == "$node" && "$maxmem" -gt "$largest_mem" ]]; then
            largest_mem=$maxmem
            largest_vmid=$vmid
        fi
    done < <(echo "$json" | jq -r '.[] | select(.type=="qemu") | "\(.vmid)|\(.maxmem)|\(.node)"')

    echo "$largest_vmid"
}

# Dengeleme kontrolü
check_balance() {
    local max_diff=0
    local loads=()

    for node in $NODES; do
        local load=$(get_node_mem_percent "$node")
        loads+=("$node:$load%")
    done

    log "INFO" "Node yükleri: ${loads[*]}" >&2

    local most_loaded=$(find_most_loaded_node)
    local least_loaded=$(find_least_loaded_node)
    local most_load=$(get_node_mem_percent "$most_loaded")
    local least_load=$(get_node_mem_percent "$least_loaded")

    max_diff=$((most_load - least_load))

    echo "$max_diff"
}

# Ana dengeleme fonksiyonu
balance_cluster() {
    log "INFO" "=========================================="
    log "INFO" "Proxmox Load Balancer başlatıldı"
    log "INFO" "=========================================="

    local diff=$(check_balance)
    local iteration=0

    while [[ "$diff" -gt "$THRESHOLD" && "$iteration" -lt "$MAX_MIGRATIONS" ]]; do
        log "INFO" "Dengesizlik tespit edildi: %$diff (Eşik: %$THRESHOLD)"

        local most_loaded=$(find_most_loaded_node)
        local least_loaded=$(find_least_loaded_node)

        log "INFO" "En yüklü: $most_loaded, En az yüklü: $least_loaded"

        # En yüklü node'dan bir VM seç
        local vmid=$(find_largest_vm_on_node "$most_loaded")

        if [[ -n "$vmid" ]]; then
            migrate_vm "$vmid" "$least_loaded"

            # Migration tamamlanmasını bekle
            log "INFO" "Migration bekleniyor... (${MIGRATION_WAIT}s)"
            sleep "$MIGRATION_WAIT"
        else
            log "WARN" "Taşınabilir VM bulunamadı"
            break
        fi

        diff=$(check_balance)
        ((iteration++))
    done

    if [[ "$diff" -le "$THRESHOLD" ]]; then
        log "INFO" "Cluster dengeli durumda (%$diff <= %$THRESHOLD)"
    else
        log "WARN" "Maksimum migration sayısına ulaşıldı ($MAX_MIGRATIONS)"
    fi

    # Son durum raporu
    print_status
}

# Durum raporu
print_status() {
    log "INFO" "=========================================="
    log "INFO" "CLUSTER DURUM RAPORU"
    log "INFO" "=========================================="

    echo ""
    echo "NODE KAYNAK KULLANIMI:"
    echo "----------------------"
    printf "%-10s %-15s %-15s %-10s %-10s\n" "Node" "RAM Kullanım" "RAM Toplam" "Yüzde" "VM Sayısı"
    echo "--------------------------------------------------------------"

    local json=$(get_node_resources)
    for node in $NODES; do
        local mem=$(echo "$json" | jq -r ".[] | select(.node==\"$node\") | .mem")
        local maxmem=$(echo "$json" | jq -r ".[] | select(.node==\"$node\") | .maxmem")
        local percent=$(get_node_mem_percent "$node")
        local vm_count=$(get_node_vm_count "$node")

        local mem_gb=$((mem / 1024 / 1024 / 1024))
        local maxmem_gb=$((maxmem / 1024 / 1024 / 1024))

        printf "%-10s %-15s %-15s %-10s %-10s\n" "$node" "${mem_gb}GB" "${maxmem_gb}GB" "%${percent}" "$vm_count"
    done

    echo ""
    echo "VM DAĞILIMI:"
    echo "------------"
    ha-manager status 2>/dev/null | grep "service vm:" | sort
    echo ""
}

# Dry-run modu
dry_run() {
    log "INFO" "DRY-RUN MODU - Değişiklik yapılmayacak"
    print_status

    local diff=$(check_balance)
    if [[ "$diff" -gt "$THRESHOLD" ]]; then
        log "INFO" "Dengesizlik tespit edildi: %$diff"
        log "INFO" "Önerilen taşımalar:"

        local most_loaded=$(find_most_loaded_node)
        local least_loaded=$(find_least_loaded_node)
        local vmid=$(find_largest_vm_on_node "$most_loaded")

        if [[ -n "$vmid" ]]; then
            log "INFO" "  - VM $vmid: $most_loaded -> $least_loaded"
        fi
    else
        log "INFO" "Cluster zaten dengeli (%$diff <= %$THRESHOLD)"
    fi
}

# Kullanım bilgisi
usage() {
    echo "Kullanım: $0 [SEÇENEK]"
    echo ""
    echo "Seçenekler:"
    echo "  balance     Cluster'ı dengele (varsayılan)"
    echo "  status      Durum raporu göster"
    echo "  dry-run     Test modu (değişiklik yapmaz)"
    echo "  help        Bu yardım mesajını göster"
    echo ""
}

# Ana program
main() {
    case "${1:-balance}" in
        balance)
            balance_cluster
            ;;
        status)
            print_status
            ;;
        dry-run)
            dry_run
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            echo "Bilinmeyen seçenek: $1"
            usage
            exit 1
            ;;
    esac
}

main "$@"
