# Proxmox Load Balancer

Automatic VM distribution and load balancing script for Proxmox VE clusters.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Proxmox VE](https://img.shields.io/badge/Proxmox%20VE-7.x%20%7C%208.x-orange)](https://www.proxmox.com/)
[![Shell Script](https://img.shields.io/badge/Shell-Bash-green)](https://www.gnu.org/software/bash/)

## Features

- **Automatic Balancing**: Distributes VMs across nodes based on RAM usage
- **HA Integration**: Fully compatible with Proxmox HA Manager
- **Flexible Configuration**: Customizable thresholds, excluded VMs, and more
- **Dry-Run Mode**: Test changes before applying them
- **Detailed Logging**: Keeps track of all operations
- **Cron Support**: Ready for automatic scheduling

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Proxmox Cluster                      │
├─────────────┬─────────────┬─────────────────────────────┤
│    Node1    │    Node2    │           Node3             │
│   (12%)     │   (14%)     │          (20%)              │
│             │             │                             │
│  ┌───────┐  │  ┌───────┐  │  ┌───────┐  ┌───────┐      │
│  │ VM A  │  │  │ VM D  │  │  │ VM G  │  │ VM H  │ ...  │
│  │ VM B  │  │  │ VM E  │  │  │ VM I  │  │ VM J  │      │
│  │ VM C  │  │  │ VM F  │  │  │ VM K  │  │ VM L  │      │
│  └───────┘  │  └───────┘  │  └───────┘  └───────┘      │
└─────────────┴─────────────┴─────────────────────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │   Shared Storage        │
        │   (NFS/Ceph/etc.)       │
        └─────────────────────────┘
```

## Requirements

- Proxmox VE 7.x or 8.x
- HA Manager enabled
- Shared storage (NFS, Ceph, etc.)
- Root access
- `jq` package (auto-installed if missing)

## Quick Start

### 1. Clone the Repository

```bash
# On your Proxmox node
git clone https://github.com/cemal-demirci/proxmox-loadbalancer.git /opt/proxmox-loadbalancer
```

### 2. Configure

```bash
# Edit configuration
nano /opt/proxmox-loadbalancer/config.cfg
```

Key settings:
```bash
# Define your cluster nodes
NODES="node1 node2 node3"

# Balancing threshold (percentage)
THRESHOLD=15

# VMs that should not be migrated (e.g., USB passthrough)
EXCLUDED_VMS=(
    100     # VM with USB device
)
```

### 3. Make Executable

```bash
chmod +x /opt/proxmox-loadbalancer/proxmox-loadbalancer.sh
```

### 4. Test

```bash
# Check cluster status
./proxmox-loadbalancer.sh status

# Dry-run (no changes)
./proxmox-loadbalancer.sh dry-run
```

### 5. Schedule (Optional)

```bash
# Run every 6 hours
echo "0 */6 * * * /opt/proxmox-loadbalancer/proxmox-loadbalancer.sh balance >> /var/log/proxmox-loadbalancer.log 2>&1" | crontab -
```

## Usage

| Command | Description |
|---------|-------------|
| `./proxmox-loadbalancer.sh status` | Show cluster status report |
| `./proxmox-loadbalancer.sh dry-run` | Test mode (no changes) |
| `./proxmox-loadbalancer.sh balance` | Balance the cluster |
| `./proxmox-loadbalancer.sh help` | Show help message |

### Example Output

```
==========================================
CLUSTER STATUS REPORT
==========================================

NODE RESOURCE USAGE:
----------------------
Node       RAM Usage      RAM Total       Percent    VM Count
--------------------------------------------------------------
Node1      92GB           754GB           12%        5
Node2      105GB          754GB           14%        5
Node3      152GB          754GB           20%        14

VM DISTRIBUTION:
------------
service vm:102 (Node3, started)
service vm:110 (Node2, started)
service vm:111 (Node1, started)
...
```

## Configuration Reference

### Node Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `NODES` | Space-separated list of cluster nodes | `"node1 node2 node3"` |
| `PREFERRED_NODE` | Preferred node (e.g., storage server) | `""` |

### Balancing Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `THRESHOLD` | Balance threshold (%) | `15` |
| `MAX_MIGRATIONS` | Max migrations per run | `5` |
| `MIGRATION_WAIT` | Wait time between migrations (sec) | `120` |

### Excluded VMs

```bash
EXCLUDED_VMS=(
    500     # VM with USB passthrough
    100     # Critical VM that shouldn't move
)
```

### Log Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `LOG_FILE` | Log file path | `/var/log/proxmox-loadbalancer.log` |
| `LOG_LEVEL` | Log level (DEBUG, INFO, WARN, ERROR) | `INFO` |

## How It Works

1. **Check Balance**: Calculates RAM usage percentage for each node
2. **Find Imbalance**: Compares highest and lowest loaded nodes
3. **Select VM**: Picks the largest VM from the most loaded node (excluding protected VMs)
4. **Migrate**: Uses HA Manager to migrate VM to least loaded node
5. **Wait**: Waits for migration to complete
6. **Repeat**: Continues until balanced or max migrations reached

## Troubleshooting

### Migration Fails

1. **Check NFS Mount**
```bash
# Verify on all nodes
mount | grep nfs-storage
```

2. **Check HA Status**
```bash
ha-manager status
```

3. **Check Logs**
```bash
tail -f /var/log/proxmox-loadbalancer.log
journalctl -u pve-ha-lrm -f
```

### Node Unreachable

```bash
# Test node connectivity
ping node2
ssh root@node2 hostname
```

### VM Cannot Be Migrated

- USB passthrough? Add to `EXCLUDED_VMS`
- Local disk? Move to shared storage
- Check HA group restrictions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Zero Density IT Team** - 2025

---

*Made with love for the Proxmox community*
