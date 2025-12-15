#!/usr/bin/env python3
"""Proxmox Load Balancer Dashboard v2.0"""
from flask import Flask, render_template, jsonify
import subprocess, json, time
from datetime import datetime

app = Flask(__name__)
_cache = {}

def cached(key, ttl=15):
    def dec(f):
        def w(*a,**k):
            now=time.time()
            if key in _cache and now-_cache[key]["t"]<ttl: return _cache[key]["v"]
            r=f(*a,**k); _cache[key]={"v":r,"t":now}; return r
        return w
    return dec

def pvesh(cmd):
    try:
        r=subprocess.run(f"pvesh {cmd} --output-format json",shell=True,capture_output=True,text=True,timeout=30)
        return json.loads(r.stdout) if r.returncode==0 else None
    except: return None

def fmt(b):
    for u in["B","KB","MB","GB","TB"]:
        if b<1024: return f"{b:.1f} {u}"
        b/=1024
    return f"{b:.1f} PB"

@cached("res")
def get_res(): return pvesh("get /cluster/resources") or []

def get_nodes():
    nodes=[]
    for r in get_res():
        if r.get("type")=="node" and r.get("status")=="online":
            nodes.append({"name":r["node"],"status":r["status"],"cpu":round(r.get("cpu",0)*100,1),"maxcpu":r.get("maxcpu",1),
                "mem":r.get("mem",0),"maxmem":r.get("maxmem",1),"mem_percent":round(r.get("mem",0)/r.get("maxmem",1)*100,1),
                "mem_gb":f"{r.get('mem',0)/1024**3:.1f}/{r.get('maxmem',0)/1024**3:.0f} GB",
                "disk_percent":round(r.get("disk",0)/r.get("maxdisk",1)*100,1),"uptime":r.get("uptime",0),
                "uptime_str":f"{r.get('uptime',0)//86400}d {(r.get('uptime',0)%86400)//3600}h","vm_count":0,"ct_count":0})
    for r in get_res():
        for n in nodes:
            if n["name"]==r["node"]:
                if r.get("type")=="qemu": n["vm_count"]+=1
                elif r.get("type")=="lxc": n["ct_count"]+=1
    return nodes

def get_guests():
    guests=[]
    for r in get_res():
        if r.get("type") in["qemu","lxc"]:
            m,mm=r.get("mem",0),r.get("maxmem",1)
            guests.append({"vmid":r["vmid"],"name":r.get("name",""),"node":r["node"],
                "type":"VM" if r["type"]=="qemu" else "CT","status":r.get("status",""),
                "cpu":round(r.get("cpu",0)*100,1),"cores":r.get("maxcpu",1),
                "mem_percent":round(m/max(mm,1)*100,1),"mem_str":f"{fmt(m)}/{fmt(mm)}",
                "disk_str":fmt(r.get("maxdisk",0)),"tags":r.get("tags","")})
    return sorted(guests,key=lambda x:(-1 if x["status"]=="running" else 1,x["vmid"]))

def get_summary():
    nodes,guests=get_nodes(),get_guests()
    if not nodes: return None
    running=[g for g in guests if g["status"]=="running"]
    mp=[n["mem_percent"] for n in nodes]; avg=sum(mp)/len(mp)
    var=sum((x-avg)**2 for x in mp)/len(mp) if len(nodes)>1 else 0
    return {"node_count":len(nodes),"vm_count":sum(1 for g in guests if g["type"]=="VM"),
        "ct_count":sum(1 for g in guests if g["type"]=="CT"),"total":len(guests),
        "running":len(running),"stopped":len(guests)-len(running),
        "avg_cpu":round(sum(n["cpu"] for n in nodes)/len(nodes),1),
        "avg_mem":round(sum(n["mem_percent"] for n in nodes)/len(nodes),1),
        "balance":round(max(0,100-var),1),"max_diff":round(max(mp)-min(mp),1) if mp else 0,
        "balanced":(max(mp)-min(mp))<15 if mp else True,"time":datetime.now().strftime("%H:%M:%S"),
        "top_cpu":sorted(running,key=lambda x:x["cpu"],reverse=True)[:5],
        "top_mem":sorted(running,key=lambda x:x["mem_percent"],reverse=True)[:5]}

def get_recs():
    nodes=get_nodes()
    if len(nodes)<2: return [{"type":"success","title":"OK","msg":"Cluster dengeli"}]
    recs=[]; avg=sum(n["mem_percent"] for n in nodes)/len(nodes)
    for n in nodes:
        d=n["mem_percent"]-avg
        if d>20: recs.append({"type":"danger","title":f"{n['name']} KRITIK","msg":f"RAM {n['mem_percent']:.0f}%"})
        elif d>15: recs.append({"type":"warning","title":f"{n['name']} Yuksek","msg":f"RAM {n['mem_percent']:.0f}%"})
        elif d<-15: recs.append({"type":"info","title":f"{n['name']} Bos","msg":f"RAM {n['mem_percent']:.0f}%"})
    return recs or [{"type":"success","title":"Saglikli","msg":"Sistemler normal"}]

@app.route("/")
def index(): return render_template("index.html")
@app.route("/api/summary")
def api_sum(): return jsonify(get_summary())
@app.route("/api/nodes")
def api_n(): return jsonify(get_nodes())
@app.route("/api/guests")
def api_g(): return jsonify(get_guests())
@app.route("/api/recommendations")
def api_r(): return jsonify(get_recs())
@app.route("/api/distribution")
def api_d():
    n=get_nodes()
    return jsonify({"labels":[x["name"] for x in n],"vm_counts":[x["vm_count"] for x in n],
        "ct_counts":[x["ct_count"] for x in n],"mem_usage":[x["mem_percent"] for x in n],
        "cpu_usage":[x["cpu"] for x in n],"disk_usage":[x["disk_percent"] for x in n]})
@app.route("/api/top")
def api_t():
    g=[x for x in get_guests() if x["status"]=="running"]
    return jsonify({"cpu":sorted(g,key=lambda x:x["cpu"],reverse=True)[:10],
        "mem":sorted(g,key=lambda x:x["mem_percent"],reverse=True)[:10]})

if __name__=="__main__": app.run(host="0.0.0.0",port=5000,debug=False)
