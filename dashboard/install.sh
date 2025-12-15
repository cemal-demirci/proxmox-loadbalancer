#!/bin/bash
echo "Installing Proxmox LB Dashboard..."
pip3 install flask
cp -r dashboard /opt/proxmox-loadbalancer/
echo "Run: python3 /opt/proxmox-loadbalancer/dashboard/app.py"
