#!/usr/bin/env python3
"""
Proxmox Load Balancer - Auto Balance Engine v2.0
Cemal Demirci | github.com/cemal-demirci

Usage:
  ./balancer.py              # Run balancing
  ./balancer.py --dry-run    # Test mode (no changes)
  ./balancer.py --status     # Show cluster status
  ./balancer.py --force      # Force run even if balanced
"""

import subprocess
import json
import sys
import os
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import yaml

# Configuration
CONFIG_FILE = '/opt/proxmox-loadbalancer/config.yaml'
LOG_FILE = '/var/log/proxmox-loadbalancer.log'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger(__name__)

# Colors for terminal
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def color(text: str, c: str) -> str:
    return f"{c}{text}{Colors.NC}"

def load_config() -> dict:
    """Load configuration from YAML file"""
    defaults = {
        'enabled': True,
        'mode': 'combined',
        'threshold': 15,
        'interval': 15,
        'dry_run': False,
        'cpu_enabled': True,
        'cpu_threshold': 80,
        'cpu_weight': 1.0,
        'memory_enabled': True,
        'memory_threshold': 85,
        'memory_weight': 2.0,
        'disk_enabled': True,
        'disk_threshold': 85,
        'disk_weight': 1.0,
        'storage_enabled': True,
        'storage_threshold': 80,
        'storage_weight': 1.5,
        'migration_type': 'online',
        'max_migrations': 3,
        'with_local_disks': False,
        'migration_bandwidth': 0,
        'migration_timeout': 300,
        'exclude_vmids': '',
        'exclude_tags': 'kritik,pinned,no-migrate',
        'exclude_nodes': '',
        'exclude_names': '',
        'notify_webhook': False,
        'notify_webhook_url': ''
    }

    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = yaml.safe_load(f) or {}
                defaults.update(config)
    except Exception as e:
        log.warning(f"Could not load config: {e}")

    return defaults

def pvesh(cmd: str) -> Optional[dict]:
    """Execute pvesh command and return JSON result"""
    try:
        result = subprocess.run(
            f"pvesh {cmd} --output-format json",
            shell=True, capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        log.error(f"pvesh error: {result.stderr}")
    except Exception as e:
        log.error(f"pvesh exception: {e}")
    return None

def get_cluster_resources() -> List[dict]:
    """Get all cluster resources"""
    return pvesh("get /cluster/resources") or []

def get_nodes(resources: List[dict]) -> List[dict]:
    """Extract online node information"""
    nodes = []
    for r in resources:
        if r.get('type') == 'node' and r.get('status') == 'online':
            mem = r.get('mem', 0)
            maxmem = r.get('maxmem', 1)
            disk = r.get('disk', 0)
            maxdisk = r.get('maxdisk', 1)

            nodes.append({
                'name': r['node'],
                'cpu': round(r.get('cpu', 0) * 100, 1),
                'mem_percent': round(mem / maxmem * 100, 1) if maxmem else 0,
                'mem_used': mem,
                'mem_total': maxmem,
                'disk_percent': round(disk / maxdisk * 100, 1) if maxdisk else 0,
                'vm_count': 0,
                'vms': []
            })
    return nodes

def get_vms(resources: List[dict], config: dict) -> List[dict]:
    """Extract VM information with filtering"""
    vms = []

    # Parse exclusions
    exclude_vmids = set()
    if config.get('exclude_vmids'):
        exclude_vmids = set(int(x.strip()) for x in str(config['exclude_vmids']).split(',') if x.strip().isdigit())

    exclude_tags = set()
    if config.get('exclude_tags'):
        exclude_tags = set(x.strip().lower() for x in str(config['exclude_tags']).split(',') if x.strip())

    exclude_names = []
    if config.get('exclude_names'):
        exclude_names = [x.strip().lower() for x in str(config['exclude_names']).split(',') if x.strip()]

    for r in resources:
        if r.get('type') not in ['qemu', 'lxc']:
            continue

        vmid = r.get('vmid')
        name = r.get('name', '')
        tags = r.get('tags', '')
        status = r.get('status', '')

        # Skip stopped VMs
        if status != 'running':
            continue

        # Apply exclusions
        if vmid in exclude_vmids:
            log.debug(f"Excluding VM {vmid} (in exclude list)")
            continue

        if tags:
            vm_tags = set(t.strip().lower() for t in tags.split(';'))
            if vm_tags & exclude_tags:
                log.debug(f"Excluding VM {vmid} (tag match: {vm_tags & exclude_tags})")
                continue

        if any(pattern in name.lower() for pattern in exclude_names):
            log.debug(f"Excluding VM {vmid} (name match)")
            continue

        mem = r.get('mem', 0)
        maxmem = r.get('maxmem', 1)

        vms.append({
            'vmid': vmid,
            'name': name,
            'node': r.get('node'),
            'type': r.get('type'),
            'status': status,
            'cpu': round(r.get('cpu', 0) * 100, 1),
            'mem': mem,
            'maxmem': maxmem,
            'mem_percent': round(mem / maxmem * 100, 1) if maxmem else 0,
            'tags': tags
        })

    return vms

def calculate_node_score(node: dict, config: dict) -> float:
    """Calculate weighted score for a node"""
    mode = config.get('mode', 'combined')

    if mode == 'memory':
        return node['mem_percent']
    elif mode == 'cpu':
        return node['cpu']
    elif mode == 'disk':
        return node['disk_percent']
    else:  # combined
        cpu_weight = config.get('cpu_weight', 1.0)
        mem_weight = config.get('memory_weight', 2.0)
        disk_weight = config.get('disk_weight', 1.0)

        total_weight = cpu_weight + mem_weight + disk_weight

        score = (
            node['cpu'] * cpu_weight +
            node['mem_percent'] * mem_weight +
            node['disk_percent'] * disk_weight
        ) / total_weight

        return round(score, 1)

def find_migration_candidates(nodes: List[dict], vms: List[dict], config: dict) -> List[Tuple[dict, dict, dict]]:
    """Find VMs to migrate and their target nodes"""
    migrations = []
    threshold = config.get('threshold', 15)
    max_migrations = config.get('max_migrations', 3)

    # Calculate scores for all nodes
    for node in nodes:
        node['score'] = calculate_node_score(node, config)
        node['vms'] = [v for v in vms if v['node'] == node['name']]
        node['vm_count'] = len(node['vms'])

    # Sort by score
    nodes_sorted = sorted(nodes, key=lambda x: x['score'], reverse=True)

    if len(nodes_sorted) < 2:
        return []

    avg_score = sum(n['score'] for n in nodes) / len(nodes)
    max_score = nodes_sorted[0]['score']
    min_score = nodes_sorted[-1]['score']
    score_diff = max_score - min_score

    log.info(f"Cluster scores - Max: {max_score:.1f}%, Min: {min_score:.1f}%, Avg: {avg_score:.1f}%, Diff: {score_diff:.1f}%")

    if score_diff < threshold:
        log.info(f"Cluster is balanced (diff {score_diff:.1f}% < threshold {threshold}%)")
        return []

    # Find migrations
    source_node = nodes_sorted[0]  # Most loaded
    target_node = nodes_sorted[-1]  # Least loaded

    # Sort VMs by memory usage (migrate larger VMs first for bigger impact)
    source_vms = sorted(source_node['vms'], key=lambda x: x['mem'], reverse=True)

    for vm in source_vms:
        if len(migrations) >= max_migrations:
            break

        # Check if migration would help
        vm_mem_gb = vm['mem'] / (1024**3)
        source_mem_after = source_node['mem_percent'] - (vm['mem'] / source_node['mem_used'] * source_node['mem_percent']) if source_node['mem_used'] else 0

        # Only migrate if it makes a meaningful difference
        if vm_mem_gb < 1:  # Skip VMs smaller than 1GB
            continue

        migrations.append((vm, source_node, target_node))
        log.info(f"Migration candidate: VM {vm['vmid']} ({vm['name']}) from {source_node['name']} to {target_node['name']}")

    return migrations

def check_vm_migratable(vmid: int, node: str, config: dict) -> Tuple[bool, str]:
    """Check if a VM can be migrated"""
    # Get VM config
    vm_config = pvesh(f"get /nodes/{node}/qemu/{vmid}/config")
    if not vm_config:
        return False, "Could not get VM config"

    # Check for local disks (if not allowed)
    if not config.get('with_local_disks', False):
        for key, value in vm_config.items():
            if key.startswith(('scsi', 'sata', 'ide', 'virtio')) and isinstance(value, str):
                if 'local' in value.lower() and 'local-lvm' not in value.lower():
                    return False, f"VM has local disk: {key}"

    # Check for USB passthrough
    for key, value in vm_config.items():
        if key.startswith('usb') and value:
            return False, f"VM has USB passthrough: {key}"

    # Check for PCI passthrough
    for key, value in vm_config.items():
        if key.startswith('hostpci') and value:
            return False, f"VM has PCI passthrough: {key}"

    return True, "OK"

def migrate_vm(vmid: int, source: str, target: str, config: dict, dry_run: bool = False) -> bool:
    """Execute VM migration"""
    migration_type = config.get('migration_type', 'online')
    timeout = config.get('migration_timeout', 300)
    bandwidth = config.get('migration_bandwidth', 0)
    with_local_disks = config.get('with_local_disks', False)

    # Build migration command
    cmd_parts = [f"create /nodes/{source}/qemu/{vmid}/migrate"]
    cmd_parts.append(f"-target {target}")

    if migration_type == 'online':
        cmd_parts.append("-online 1")

    if with_local_disks:
        cmd_parts.append("-with-local-disks 1")

    if bandwidth > 0:
        cmd_parts.append(f"-bwlimit {bandwidth}")

    cmd = " ".join(cmd_parts)

    if dry_run:
        log.info(f"[DRY-RUN] Would execute: pvesh {cmd}")
        return True

    log.info(f"Starting migration: VM {vmid} from {source} to {target}")

    try:
        result = subprocess.run(
            f"pvesh {cmd}",
            shell=True, capture_output=True, text=True, timeout=timeout
        )

        if result.returncode == 0:
            log.info(f"Migration started successfully for VM {vmid}")

            # Wait for migration to complete
            for i in range(timeout // 10):
                time.sleep(10)
                resources = get_cluster_resources()
                for r in resources:
                    if r.get('vmid') == vmid:
                        if r.get('node') == target:
                            log.info(f"Migration completed: VM {vmid} is now on {target}")
                            return True
                        break

            log.warning(f"Migration timeout for VM {vmid}")
            return False
        else:
            log.error(f"Migration failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        log.error(f"Migration command timed out for VM {vmid}")
        return False
    except Exception as e:
        log.error(f"Migration exception: {e}")
        return False

def send_notification(message: str, config: dict):
    """Send webhook notification"""
    if not config.get('notify_webhook') or not config.get('notify_webhook_url'):
        return

    try:
        import urllib.request
        import urllib.parse

        data = json.dumps({
            'text': f"[Proxmox Load Balancer] {message}",
            'username': 'ProxLB'
        }).encode('utf-8')

        req = urllib.request.Request(
            config['notify_webhook_url'],
            data=data,
            headers={'Content-Type': 'application/json'}
        )

        urllib.request.urlopen(req, timeout=10)
        log.info("Notification sent")
    except Exception as e:
        log.warning(f"Failed to send notification: {e}")

def print_status(nodes: List[dict], config: dict):
    """Print cluster status"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}  PROXMOX CLUSTER STATUS{Colors.NC}")
    print(f"{Colors.BLUE}{'='*60}{Colors.NC}\n")

    for node in sorted(nodes, key=lambda x: x['score'], reverse=True):
        score_color = Colors.GREEN if node['score'] < 50 else Colors.YELLOW if node['score'] < 75 else Colors.RED

        print(f"  {Colors.BOLD}{node['name']}{Colors.NC}")
        print(f"    Score: {score_color}{node['score']:.1f}%{Colors.NC}")
        print(f"    CPU:   {node['cpu']:.1f}%")
        print(f"    RAM:   {node['mem_percent']:.1f}%")
        print(f"    Disk:  {node['disk_percent']:.1f}%")
        print(f"    VMs:   {node['vm_count']}")
        print()

    avg_score = sum(n['score'] for n in nodes) / len(nodes) if nodes else 0
    max_diff = max(n['score'] for n in nodes) - min(n['score'] for n in nodes) if nodes else 0
    threshold = config.get('threshold', 15)

    status = color("BALANCED", Colors.GREEN) if max_diff < threshold else color("IMBALANCED", Colors.YELLOW)

    print(f"  Average Score: {avg_score:.1f}%")
    print(f"  Max Difference: {max_diff:.1f}%")
    print(f"  Threshold: {threshold}%")
    print(f"  Status: {status}")
    print(f"\n{Colors.BLUE}{'='*60}{Colors.NC}\n")

def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args or '-n' in args
    show_status = '--status' in args or '-s' in args
    force = '--force' in args or '-f' in args

    print(f"\n{Colors.CYAN}╔══════════════════════════════════════════════════════════╗{Colors.NC}")
    print(f"{Colors.CYAN}║     Proxmox Load Balancer - Auto Balance Engine v2.0    ║{Colors.NC}")
    print(f"{Colors.CYAN}║     Cemal Demirci | github.com/cemal-demirci            ║{Colors.NC}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════╝{Colors.NC}\n")

    config = load_config()

    if not config.get('enabled', True):
        log.info("Load balancer is disabled in config")
        return 0

    if dry_run:
        log.info("Running in DRY-RUN mode (no changes will be made)")
        config['dry_run'] = True

    # Get cluster data
    log.info("Fetching cluster resources...")
    resources = get_cluster_resources()
    if not resources:
        log.error("Could not fetch cluster resources")
        return 1

    nodes = get_nodes(resources)
    if len(nodes) < 2:
        log.info("Single node cluster - no balancing needed")
        return 0

    vms = get_vms(resources, config)
    log.info(f"Found {len(nodes)} nodes and {len(vms)} running VMs")

    # Calculate scores
    for node in nodes:
        node['score'] = calculate_node_score(node, config)
        node['vms'] = [v for v in vms if v['node'] == node['name']]
        node['vm_count'] = len(node['vms'])

    if show_status:
        print_status(nodes, config)
        return 0

    # Find migration candidates
    migrations = find_migration_candidates(nodes, vms, config)

    if not migrations and not force:
        log.info("No migrations needed - cluster is balanced")
        print_status(nodes, config)
        return 0

    # Execute migrations
    successful = 0
    failed = 0

    for vm, source, target in migrations:
        vmid = vm['vmid']

        # Check if migratable
        can_migrate, reason = check_vm_migratable(vmid, source['name'], config)
        if not can_migrate:
            log.warning(f"Skipping VM {vmid}: {reason}")
            continue

        # Execute migration
        if migrate_vm(vmid, source['name'], target['name'], config, dry_run):
            successful += 1
            send_notification(f"Migrated VM {vmid} ({vm['name']}) from {source['name']} to {target['name']}", config)
        else:
            failed += 1

    # Summary
    log.info(f"Migration summary: {successful} successful, {failed} failed")

    if successful > 0:
        send_notification(f"Balancing complete: {successful} VMs migrated", config)

    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
