#!/bin/bash
#
# Proxmox Load Balancer - Cluster Installer
# Cemal Demirci | github.com/cemal-demirci
#
# Usage: curl -sSL https://raw.githubusercontent.com/cemal-demirci/proxmox-loadbalancer/master/install.sh | bash
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         Proxmox Load Balancer Installer v2.0              ║"
echo "║         Cemal Demirci | github.com/cemal-demirci          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

[ "$EUID" -ne 0 ] && { echo -e "${RED}Error: Please run as root${NC}"; exit 1; }
[ ! -d /etc/pve ] && { echo -e "${RED}Error: Not a Proxmox VE node${NC}"; exit 1; }

GITHUB_RAW="https://raw.githubusercontent.com/cemal-demirci/proxmox-loadbalancer/master"
INSTALL_DIR="/opt/proxmox-loadbalancer"
JS_FILE="/usr/share/pve-manager/js/proxlb-panel.js"
HTML_TPL="/usr/share/pve-manager/index.html.tpl"

get_cluster_nodes() {
    [ -f /etc/pve/corosync.conf ] && grep -oP 'ring0_addr:\s*\K[0-9.]+' /etc/pve/corosync.conf 2>/dev/null || hostname -I | awk '{print $1}'
}

echo -e "${YELLOW}[1/6] Detecting cluster nodes...${NC}"
NODES=$(get_cluster_nodes)
CURRENT_IP=$(hostname -I | awk '{print $1}')
echo -e "  Found: $NODES"

echo -e "${YELLOW}[2/6] Creating directories...${NC}"
mkdir -p $INSTALL_DIR/dashboard/templates

echo -e "${YELLOW}[3/7] Downloading files...${NC}"
curl -sSL "$GITHUB_RAW/dashboard/app.py" -o "$INSTALL_DIR/dashboard/app.py"
curl -sSL "$GITHUB_RAW/dashboard/templates/index.html" -o "$INSTALL_DIR/dashboard/templates/index.html"
curl -sSL "$GITHUB_RAW/balancer.py" -o "$INSTALL_DIR/balancer.py"
curl -sSL "$GITHUB_RAW/ui/proxlb-panel.js" -o "/tmp/proxlb-panel.js"
chmod +x "$INSTALL_DIR/balancer.py"
echo -e "  ${GREEN}Downloaded${NC}"

echo -e "${YELLOW}[4/6] Installing dependencies...${NC}"
apt-get update -qq && apt-get install -y -qq python3-flask python3-yaml >/dev/null 2>&1
echo -e "  ${GREEN}Done${NC}"

echo -e "${YELLOW}[5/6] Deploying to cluster nodes...${NC}"
for node in $NODES; do
    if [ "$node" == "$CURRENT_IP" ]; then
        echo -e "  $node (local)..."
        cp /tmp/proxlb-panel.js $JS_FILE
        grep -q "proxlb-panel.js" $HTML_TPL || sed -i '/<\/head>/i <script type="text/javascript" src="/pve2/js/proxlb-panel.js"></script>' $HTML_TPL
        systemctl restart pveproxy
    else
        echo -e "  $node (remote)..."
        scp -o StrictHostKeyChecking=no -o ConnectTimeout=5 /tmp/proxlb-panel.js root@$node:$JS_FILE 2>/dev/null && \
        ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$node "grep -q 'proxlb-panel.js' $HTML_TPL || sed -i '/<\\/head>/i <script type=\"text/javascript\" src=\"/pve2/js/proxlb-panel.js\"></script>' $HTML_TPL; systemctl restart pveproxy" 2>/dev/null || echo -e "    ${RED}Failed${NC}"
    fi
done
echo -e "  ${GREEN}Done${NC}"

echo -e "${YELLOW}[6/6] Setting up dashboard service...${NC}"
cat > /etc/systemd/system/proxlb-dashboard.service << 'EOF'
[Unit]
Description=Proxmox Load Balancer Dashboard
After=network.target
[Service]
Type=simple
WorkingDirectory=/opt/proxmox-loadbalancer/dashboard
ExecStart=/usr/bin/python3 /opt/proxmox-loadbalancer/dashboard/app.py
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload && systemctl enable proxlb-dashboard >/dev/null 2>&1 && systemctl restart proxlb-dashboard
sleep 2
systemctl is-active --quiet proxlb-dashboard && echo -e "  ${GREEN}Service started${NC}" || echo -e "  ${RED}Service failed${NC}"

rm -f /tmp/proxlb-panel.js

echo -e "${YELLOW}[7/7] Setting up cron & config...${NC}"
CRON_CMD="0 */6 * * * /usr/bin/python3 $INSTALL_DIR/balancer.py >> /var/log/proxmox-loadbalancer.log 2>&1"
(crontab -l 2>/dev/null | grep -v "balancer.py"; echo "$CRON_CMD") | crontab -

[ ! -f "$INSTALL_DIR/config.yaml" ] && cat > "$INSTALL_DIR/config.yaml" << 'YAML'
enabled: true
mode: combined
threshold: 15
dry_run: false
cpu_enabled: true
cpu_threshold: 80
cpu_weight: 1.0
memory_enabled: true
memory_threshold: 85
memory_weight: 2.0
disk_enabled: true
disk_threshold: 85
disk_weight: 1.0
storage_enabled: true
storage_threshold: 80
storage_weight: 1.5
migration_type: online
max_migrations: 3
with_local_disks: false
migration_bandwidth: 0
migration_timeout: 300
exclude_vmids: ""
exclude_tags: "kritik,pinned,no-migrate"
exclude_nodes: ""
exclude_names: ""
notify_webhook: false
notify_webhook_url: ""
YAML
echo -e "  ${GREEN}Done${NC}"

echo -e "\n${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Installation Complete!                        ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Dashboard:  ${BLUE}http://$CURRENT_IP:5000${NC}"
echo -e "Balancer:   ${BLUE}$INSTALL_DIR/balancer.py${NC}"
echo -e "Config:     ${BLUE}$INSTALL_DIR/config.yaml${NC}"
echo -e "Cron:       ${BLUE}Every 6 hours${NC}"
echo ""
echo -e "${YELLOW}Commands:${NC}"
echo -e "  $INSTALL_DIR/balancer.py --status   # Cluster status"
echo -e "  $INSTALL_DIR/balancer.py --dry-run  # Test mode"
echo -e "  $INSTALL_DIR/balancer.py            # Run balancing"
echo ""
echo -e "${YELLOW}Refresh browser: Ctrl+Shift+R${NC}"
