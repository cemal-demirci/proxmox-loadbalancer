#!/usr/bin/env python3
"""
Proxmox Load Balancer Dashboard
Web-based monitoring and analytics for Proxmox clusters
"""

from flask import Flask, render_template, jsonify
import subprocess
import json
from datetime import datetime
import time

app = Flask(__name__)

CACHE_TIMEOUT = 30
_cache = {}

def cached(key, timeout=CACHE_TIMEOUT):
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = time.time()
            if key in _cache and now - _cache[key]['time'] < timeout:
                return _cache[key]['value']
            result = func(*args, **kwargs)
            _cache[key] = {'value': result, 'time': now}
            return result
        return wrapper
    return decorator

def run_pvesh(cmd):
    try:
        result = subprocess.run(
            f"pvesh {cmd} --output-format json",
            shell=True, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"Error: {e}")
    return None

@cached('resources')
def get_cluster_resources():
    return run_pvesh("get /cluster/resources")

def get_node_stats():
    resources = get_cluster_resources()
    if not resources:
        return []
    nodes = {}
    for item in resources:
        if item.get('type') == 'node' and item.get('status') == 'online':
            name = item.get('node')
            nodes[name] = {
                'name': name, 'status': 'online',
                'cpu': round(item.get('cpu', 0) * 100, 1),
                'mem': item.get('mem', 0),
                'maxmem': item.get('maxmem', 0),
                'mem_percent': round(item.get('mem', 0) / item.get('maxmem', 1) * 100, 1),
                'vm_count': 0, 'vms': []
            }
    for item in resources:
        if item.get('type') == 'qemu':
            node = item.get('node')
            if node in nodes:
                nodes[node]['vm_count'] += 1
    return list(nodes.values())

def get_cluster_summary():
    nodes = get_node_stats()
    if not nodes: return None
    total_mem = sum(n['mem'] for n in nodes)
    total_maxmem = sum(n['maxmem'] for n in nodes)
    mem_percents = [n['mem_percent'] for n in nodes]
    avg = sum(mem_percents) / len(mem_percents) if nodes else 0
    variance = sum((x - avg)**2 for x in mem_percents) / len(mem_percents) if len(nodes) > 1 else 0
    return {
        'node_count': len(nodes),
        'total_vms': sum(n['vm_count'] for n in nodes),
        'avg_cpu': round(sum(n['cpu'] for n in nodes) / len(nodes), 1),
        'balance_score': round(max(0, 100 - variance), 1),
        'last_update': datetime.now().strftime('%H:%M:%S')
    }

def get_vm_distribution():
    nodes = get_node_stats()
    return {'labels': [n['name'] for n in nodes], 'vm_counts': [n['vm_count'] for n in nodes],
            'mem_usage': [n['mem_percent'] for n in nodes], 'cpu_usage': [n['cpu'] for n in nodes]}

def get_recommendations():
    nodes = get_node_stats()
    if len(nodes) < 2: return [{'type': 'success', 'message': 'Cluster dengeli', 'action': 'Islem gerekmiyor'}]
    recs = []
    avg = sum(n['mem_percent'] for n in nodes) / len(nodes)
    for n in nodes:
        diff = n['mem_percent'] - avg
        if diff > 15: recs.append({'type': 'warning', 'message': f"{n['name']} yuklu ({n['mem_percent']}%)", 'action': 'VM tasi'})
        elif diff < -15: recs.append({'type': 'info', 'message': f"{n['name']} bos ({n['mem_percent']}%)", 'action': 'VM alabilir'})
    return recs or [{'type': 'success', 'message': 'Cluster dengeli', 'action': 'Islem gerekmiyor'}]

@app.route('/')
def index(): return render_template('index.html')
@app.route('/api/summary')
def api_summary(): return jsonify(get_cluster_summary())
@app.route('/api/nodes')
def api_nodes(): return jsonify(get_node_stats())
@app.route('/api/distribution')
def api_distribution(): return jsonify(get_vm_distribution())
@app.route('/api/recommendations')
def api_recommendations(): return jsonify(get_recommendations())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
