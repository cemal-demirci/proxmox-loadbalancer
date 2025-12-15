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

echo -e "${YELLOW}[3/6] Downloading files...${NC}"
curl -sSL "$GITHUB_RAW/dashboard/app.py" -o "$INSTALL_DIR/dashboard/app.py"
curl -sSL "$GITHUB_RAW/dashboard/templates/index.html" -o "$INSTALL_DIR/dashboard/templates/index.html"
curl -sSL "$GITHUB_RAW/ui/proxlb-panel.js" -o "/tmp/proxlb-panel.js"
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

echo -e "\n${GREEN}Installation Complete!${NC}"
echo -e "Dashboard: ${BLUE}http://$CURRENT_IP:5000${NC}"
echo -e "UI: ${BLUE}Look for 'Load Balancer' button${NC}"
echo -e "${YELLOW}Refresh browser with Ctrl+Shift+R${NC}"
