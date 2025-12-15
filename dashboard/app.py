#!/usr/bin/env python3
"""Proxmox Load Balancer Dashboard v2.0"""

from flask import Flask, render_template, jsonify, request
import subprocess
import json
import yaml
from datetime import datetime
import time

app = Flask(__name__)

_cache = {}
CACHE_TTL = 30

def cached(key):
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = time.time()
            if key in _cache and now - _cache[key]["t"] < CACHE_TTL:
                return _cache[key]["v"]
            result = func(*args, **kwargs)
            _cache[key] = {"v": result, "t": now}
            return result
        return wrapper
    return decorator

def pvesh(cmd):
    try:
        r = subprocess.run(f"pvesh {cmd} --output-format json", 
                          shell=True, capture_output=True, text=True, timeout=30)
        return json.loads(r.stdout) if r.returncode == 0 else None
    except:
        return None

@cached("resources")
def get_resources():
    return pvesh("get /cluster/resources") or []

def get_nodes():
    nodes = []
    for r in get_resources():
        if r.get("type") == "node" and r.get("status") == "online":
            nodes.append({
                "name": r["node"],
                "status": r["status"],
                "cpu": round(r.get("cpu", 0) * 100, 1),
                "maxcpu": r.get("maxcpu", 1),
                "mem": r.get("mem", 0),
                "maxmem": r.get("maxmem", 1),
                "mem_percent": round(r.get("mem", 0) / r.get("maxmem", 1) * 100, 1),
                "disk": r.get("disk", 0),
                "maxdisk": r.get("maxdisk", 1),
                "uptime": r.get("uptime", 0),
                "vm_count": 0,
                "ct_count": 0
            })
    # Count guests
    for r in get_resources():
        if r.get("type") == "qemu":
            for n in nodes:
                if n["name"] == r["node"]:
                    n["vm_count"] += 1
        elif r.get("type") == "lxc":
            for n in nodes:
                if n["name"] == r["node"]:
                    n["ct_count"] += 1
    return nodes

def get_guests():
    guests = []
    for r in get_resources():
        if r.get("type") in ["qemu", "lxc"]:
            guests.append({
                "vmid": r["vmid"],
                "name": r.get("name", ""),
                "node": r["node"],
                "type": "VM" if r["type"] == "qemu" else "CT",
                "status": r.get("status", ""),
                "cpu": round(r.get("cpu", 0) * 100, 1),
                "mem": r.get("mem", 0),
                "maxmem": r.get("maxmem", 0),
                "mem_percent": round(r.get("mem", 0) / max(r.get("maxmem", 1), 1) * 100, 1),
                "tags": r.get("tags", "")
            })
    return guests

def get_summary():
    nodes = get_nodes()
    guests = get_guests()
    if not nodes:
        return None
    
    total_mem = sum(n["mem"] for n in nodes)
    total_maxmem = sum(n["maxmem"] for n in nodes)
    mem_percents = [n["mem_percent"] for n in nodes]
    avg = sum(mem_percents) / len(mem_percents)
    variance = sum((x - avg)**2 for x in mem_percents) / len(mem_percents) if len(nodes) > 1 else 0
    
    return {
        "node_count": len(nodes),
        "vm_count": sum(1 for g in guests if g["type"] == "VM"),
        "ct_count": sum(1 for g in guests if g["type"] == "CT"),
        "total_guests": len(guests),
        "running": sum(1 for g in guests if g["status"] == "running"),
        "stopped": sum(1 for g in guests if g["status"] == "stopped"),
        "avg_cpu": round(sum(n["cpu"] for n in nodes) / len(nodes), 1),
        "avg_mem": round(total_mem / total_maxmem * 100, 1) if total_maxmem else 0,
        "balance_score": round(max(0, 100 - variance), 1),
        "max_diff": round(max(mem_percents) - min(mem_percents), 1) if mem_percents else 0,
        "is_balanced": (max(mem_percents) - min(mem_percents)) < 15 if mem_percents else True,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

def get_recommendations():
    nodes = get_nodes()
    if len(nodes) < 2:
        return [{"type": "success", "title": "Durum", "msg": "Cluster dengeli"}]
    
    recs = []
    avg = sum(n["mem_percent"] for n in nodes) / len(nodes)
    
    for n in nodes:
        diff = n["mem_percent"] - avg
        if diff > 20:
            recs.append({"type": "danger", "title": n["name"], 
                        "msg": f"Asiri yuklu! RAM: {n['mem_percent']}% (Ort: {avg:.0f}%)"})
        elif diff > 15:
            recs.append({"type": "warning", "title": n["name"],
                        "msg": f"Yuklu. RAM: {n['mem_percent']}%"})
        elif diff < -15:
            recs.append({"type": "info", "title": n["name"],
                        "msg": f"Dusuk kullanim. RAM: {n['mem_percent']}%"})
    
    if not recs:
        recs.append({"type": "success", "title": "Durum", "msg": "Cluster dengeli durumda"})
    return recs

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/summary")
def api_summary():
    return jsonify(get_summary())

@app.route("/api/nodes")
def api_nodes():
    return jsonify(get_nodes())

@app.route("/api/guests")
def api_guests():
    return jsonify(get_guests())

@app.route("/api/recommendations")
def api_recommendations():
    return jsonify(get_recommendations())

@app.route("/api/distribution")
def api_distribution():
    nodes = get_nodes()
    return jsonify({
        "labels": [n["name"] for n in nodes],
        "vm_counts": [n["vm_count"] for n in nodes],
        "ct_counts": [n["ct_count"] for n in nodes],
        "mem_usage": [n["mem_percent"] for n in nodes],
        "cpu_usage": [n["cpu"] for n in nodes]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
