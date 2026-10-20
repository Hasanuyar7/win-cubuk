import tkinter as tk
from tkinter import Toplevel, Label, messagebox, ttk, simpledialog, filedialog
import psutil
import datetime
import threading
import time
import json
import urllib.request
import urllib.error
import urllib.parse
import subprocess
import os
import sys
import tempfile
import ctypes
from ctypes import wintypes
import math
import winsound
import socket
import webbrowser
import glob
import http.server
import socketserver
import random
import re
import winreg
import xml.etree.ElementTree as ET

import pystray
from PIL import Image, ImageDraw, ImageGrab, ImageTk

try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False
    print("QR için: pip install qrcode[pil]")

try:
    import speech_recognition as sr
    ASSISTANT_AVAILABLE = True
except ImportError:
    ASSISTANT_AVAILABLE = False
    print("Kurulum: pip install SpeechRecognition pyaudio")

try:
    import edge_tts
    import asyncio
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("Kurulum: pip install edge-tts")

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Kurulum: pip install pygame")

try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL, cast, POINTER
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False

try:
    from speedtest import Speedtest
    SPEEDTEST_AVAILABLE = True
except ImportError:
    SPEEDTEST_AVAILABLE = False

try:
    from winsdk.windows.media.control import (
        GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    )
    from winsdk.windows.storage.streams import Buffer, DataReader, InputStreamOptions
    MEDIA_AVAILABLE = True
except ImportError:
    MEDIA_AVAILABLE = False
    print("Şarkı bilgisi için: pip install winsdk")

user32 = ctypes.windll.user32
HOTKEY_ID = 1
MOD_CTRL_SHIFT = 0x0002 | 0x0004
VK_N = 0x4E
MONITOR_DEFAULT_TO_PRIMARY = 1

# ============================================================
# 🔑 GROQ API ANAHTARI
# ============================================================
GROQ_API_KEY = ""
GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.3-70b-versatile",
    "gemma2-9b-it",
    "mixtral-8x7b-32768",
]

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nexus_settings.json")
QA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nexus_qa.json")
CURRENT_VERSION = "14.3"
GITHUB_REPO_API = "https://api.github.com/repos/kullaniciadi/nexus-bar/releases/latest"
ASSISTANT_NAME = "Ahmet"
ASSISTANT_VOICE_NAME = "tr-TR-AhmetNeural"
CONTROL_PORT = 8081

CONTROL_HTML = """<!DOCTYPE html>
<html lang="tr"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>🦁 Nexus Kontrol</title>
<style>
  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  body{font-family:-apple-system,'Segoe UI',sans-serif;background:#1C1C2E;color:#fff;
       margin:0;padding:16px;user-select:none;overflow-x:hidden}
  body::before{content:'';position:fixed;top:-200px;left:-200px;width:500px;height:500px;
    background:radial-gradient(circle,rgba(79,195,247,.15),transparent 70%);
    pointer-events:none;z-index:0;animation:float1 15s ease-in-out infinite}
  body::after{content:'';position:fixed;bottom:-200px;right:-200px;width:500px;height:500px;
    background:radial-gradient(circle,rgba(255,0,127,.12),transparent 70%);
    pointer-events:none;z-index:0;animation:float2 18s ease-in-out infinite}
  @keyframes float1{0%,100%{transform:translate(0,0)}50%{transform:translate(80px,60px)}}
  @keyframes float2{0%,100%{transform:translate(0,0)}50%{transform:translate(-60px,-80px)}}
  h1{color:#4FC3F7;text-align:center;font-size:20px;margin:8px 0 16px;position:relative;z-index:1}
  .nowplaying{position:relative;display:flex;align-items:center;gap:16px;
    background:rgba(26,26,62,.75);backdrop-filter:blur(20px);
    padding:16px 18px;border-radius:22px;max-width:500px;margin:0 auto 20px;overflow:hidden;
    transition:all .55s cubic-bezier(.4,0,.2,1);box-shadow:0 12px 40px rgba(0,0,0,.5);z-index:1}
  .nowplaying::before{content:'';position:absolute;inset:0;border-radius:22px;padding:1.5px;
    background:linear-gradient(135deg,#4FC3F7,#CE93D8,#FF007F,#4FC3F7);background-size:300% 300%;
    -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);
    -webkit-mask-composite:xor;mask-composite:exclude;animation:borderFlow 4s ease infinite;pointer-events:none}
  @keyframes borderFlow{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
  .nowplaying.hidden{opacity:0;transform:translateY(-30px) scale(.9);max-height:0;padding:0;margin:0;
    pointer-events:none;box-shadow:none}
  .np-cover{width:82px;height:82px;border-radius:18px;overflow:hidden;flex-shrink:0;position:relative;
    background:linear-gradient(135deg,#2A2A40,#1C1C2E);display:flex;align-items:center;justify-content:center;
    box-shadow:0 8px 30px rgba(79,195,247,.5)}
  .np-cover::after{content:'';position:absolute;inset:0;
    background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.35) 50%,transparent 70%);
    transform:translateX(-110%);animation:shine 3.2s ease-in-out infinite;pointer-events:none;border-radius:18px}
  @keyframes shine{0%{transform:translateX(-110%)}55%,100%{transform:translateX(110%)}}
  .np-cover img{width:100%;height:100%;object-fit:cover;display:none;position:absolute;top:0;left:0;border-radius:18px}
  .np-placeholder{font-size:38px;opacity:.4}
  .np-info{flex:1;min-width:0}
  .np-title{font-size:16px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:8px;
    background:linear-gradient(90deg,#4FC3F7,#CE93D8,#FF007F,#4FC3F7);background-size:300% 100%;
    -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;
    animation:titleFlow 5s ease infinite}
  @keyframes titleFlow{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
  .np-artist{font-size:12px;color:#B0B0C0;display:flex;align-items:center;gap:8px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
  .np-artist .dot{width:7px;height:7px;border-radius:50%;background:#69F0AE;box-shadow:0 0 10px #69F0AE;
    flex-shrink:0;animation:pulse 1.5s ease infinite}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
  .sys-panel{max-width:500px;margin:0 auto 16px;padding:12px 16px;border-radius:14px;
    background:rgba(42,42,64,.6);backdrop-filter:blur(10px);position:relative;z-index:1}
  .sys-bar{display:flex;align-items:center;gap:10px;font-size:11px;margin:6px 0}
  .sys-bar span:first-child{width:36px;color:#B0B0C0;font-weight:600}
  .sys-bar .bar{flex:1;height:6px;background:#1C1C2E;border-radius:4px;overflow:hidden}
  .sys-bar .fill{height:100%;width:0%;background:linear-gradient(90deg,#4FC3F7,#00E5FF);
    transition:width .5s;border-radius:4px}
  .sys-bar .fill.ram{background:linear-gradient(90deg,#CE93D8,#FF007F)}
  .sys-bar span:last-child{width:38px;text-align:right;color:#E0E0E0;font-weight:700}
  .theme-bar{max-width:500px;margin:0 auto 16px;padding:10px 16px;border-radius:14px;
    background:rgba(42,42,64,.6);backdrop-filter:blur(10px);display:flex;
    align-items:center;gap:8px;justify-content:center;position:relative;z-index:1}
  .theme-bar .label{font-size:11px;color:#B0B0C0;margin-right:4px}
  .theme-btn{width:42px;height:42px;padding:0;border-radius:12px;background:#1C1C2E;
    border:2px solid transparent;font-size:18px;display:flex;align-items:center;justify-content:center}
  .theme-btn:active{transform:scale(.9);border-color:#4FC3F7}
  .ask-box{max-width:500px;margin:0 auto 16px;display:flex;gap:8px;position:relative;z-index:1}
  .ask-box input{flex:1;padding:14px 16px;border-radius:12px;border:1px solid #3A3A5C;
    background:rgba(26,26,62,.75);color:#fff;font-size:14px;outline:none}
  .ask-box input::placeholder{color:#888}
  .ask-box button{width:52px;padding:0;border-radius:12px;background:#3A5A8C;font-size:20px}
  .ask-box button:active{background:#4FC3F7;color:#000}
  .answer{max-width:500px;margin:0 auto 16px;padding:14px 16px;border-radius:14px;
    background:rgba(79,195,247,.1);border:1px solid rgba(79,195,247,.3);
    font-size:13px;line-height:1.5;color:#E0E0E0;position:relative;z-index:1;display:none}
  .answer.show{display:block;animation:fadeIn .3s ease}
  @keyframes fadeIn{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:translateY(0)}}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;max-width:500px;margin:0 auto;position:relative;z-index:1}
  button{padding:18px 8px;border-radius:14px;border:none;font-size:15px;font-weight:600;
    background:#2A2A40;color:#fff;cursor:pointer;
    display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px}
  button:active{background:#4FC3F7;color:#000;transform:scale(.96)}
  .wide{grid-column:1/-1}
  .big{font-size:22px}
  .accent{background:#3A5A8C}
  .accent:active{background:#4FC3F7;color:#000}
  .danger{background:#8C2A2A}
  .danger:active{background:#FF5252;color:#fff}
  .status{text-align:center;font-size:11px;color:#69F0AE;margin-top:14px;min-height:16px;position:relative;z-index:1}
  .info{text-align:center;font-size:10px;color:#888;margin-top:8px;position:relative;z-index:1}
</style></head>
<body>
<h1>🦁 Nexus Bar Kontrol</h1>

<div class="nowplaying hidden" id="np-card">
  <div class="np-cover">
    <span class="np-placeholder" id="np-placeholder">🎵</span>
    <img id="np-img" src="" alt="" />
  </div>
  <div class="np-info">
    <div class="np-title" id="np-title">—</div>
    <div class="np-artist"><span class="dot"></span><span id="np-artist">Çalmıyor</span></div>
  </div>
</div>

<div class="sys-panel">
  <div class="sys-bar"><span>CPU</span><div class="bar"><div class="fill" id="cpu-fill"></div></div><span id="cpu-val">0%</span></div>
  <div class="sys-bar"><span>RAM</span><div class="bar"><div class="fill ram" id="ram-fill"></div></div><span id="ram-val">0%</span></div>
</div>

<div class="ask-box">
  <input id="ask-input" type="text" placeholder="Bir şey sor..." onkeydown="if(event.key==='Enter') askNow()">
  <button onclick="askNow()">🔍</button>
</div>
<div class="answer" id="answer-box"></div>

<div class="theme-bar">
  <span class="label">🎨</span>
  <button class="theme-btn" onclick="cmd('theme_koyu')">🌙</button>
  <button class="theme-btn" onclick="cmd('theme_acik')">☀️</button>
  <button class="theme-btn" onclick="cmd('theme_neon')">💜</button>
  <button class="theme-btn" onclick="cmd('theme_seffaf')">👻</button>
</div>

<div class="grid">
  <button onclick="cmd('playpause')"><span class="big">⏯️</span>Oynat/Duraklat</button>
  <button onclick="cmd('next')"><span class="big">⏭️</span>Sonraki</button>
  <button onclick="cmd('prev')"><span class="big">⏮️</span>Önceki</button>
  <button onclick="cmd('mute')"><span class="big">🔇</span>Sessiz</button>
  <button onclick="cmd('volup')"><span class="big">🔊</span>Ses +</button>
  <button onclick="cmd('voldown')"><span class="big">🔉</span>Ses −</button>
  <button onclick="cmd('music')"><span class="big">🎵</span>Müzik Aç</button>
  <button onclick="cmd('musicclose')"><span class="big">🔕</span>Müzik Kapat</button>
  <button onclick="cmd('screenshot')"><span class="big">📷</span>Ekran</button>
  <button onclick="cmd('clean')"><span class="big">🧹</span>Temizle</button>
  <button onclick="cmd('lock')"><span class="big">🔒</span>Kilitle</button>
  <button onclick="cmd('privacy')"><span class="big">🕶️</span>Gizlilik</button>
  <button onclick="cmd('pomodoro')"><span class="big">🍅</span>Pomodoro</button>
  <button onclick="cmd('water')"><span class="big">💧</span>Su</button>
  <button onclick="cmd('taskmgr')" class="wide"><span class="big">📋</span>Görev Yöneticisi</button>
  <button onclick="cmd('assistant')" class="wide"><span class="big">🎤</span>Asistanı Aç/Kapat</button>
  <button onclick="cmd('minimize')" class="accent wide"><span class="big">⬇️</span>Sistem Tepsisine Küçült</button>
  <button onclick="cmd('show')" class="accent wide"><span class="big">⬆️</span>Çubuğu Göster</button>
  <button onclick="cmd('quit')" class="danger wide"><span class="big">❌</span>Uygulamayı Kapat</button>
</div>
<div class="status" id="st"></div>
<div class="info">Nexus Bar v__VERSION__</div>
<script>
fetch('/connected').catch(()=>{});
let timer;
async function cmd(c){
  const st=document.getElementById('st');
  try{
    const r=await fetch('/cmd/'+c,{cache:'no-store'});
    if(!r.ok) throw new Error(r.status);
    st.textContent='✓ '+c;
    if(navigator.vibrate) navigator.vibrate(40);
  }catch(e){ st.style.color='#FF5252'; st.textContent='✗ '+e.message; }
  clearTimeout(timer);
  timer=setTimeout(()=>{st.textContent='';st.style.color='#69F0AE';},2000);
}
async function askNow(){
  const inp = document.getElementById('ask-input');
  const box = document.getElementById('answer-box');
  const q = inp.value.trim();
  if(!q) return;
  box.classList.add('show'); box.textContent = '🧠 Yapay zeka düşünüyor...';
  try{
    const r = await fetch('/ask?q=' + encodeURIComponent(q));
    const d = await r.json();
    box.textContent = d.answer || 'Yanıt bulunamadı';
  }catch(e){ box.textContent = '✗ ' + e.message; }
}
let lastCoverHash = '';
const npCard = document.getElementById('np-card');
async function updateNP(){
  try{
    const r = await fetch('/nowplaying', {cache:'no-store'});
    const d = await r.json();
    const title = document.getElementById('np-title');
    const artist = document.getElementById('np-artist');
    const img = document.getElementById('np-img');
    const ph = document.getElementById('np-placeholder');
    if(d.playing){
      npCard.classList.remove('hidden');
      title.textContent = d.title || 'Bilinmeyen parça';
      artist.textContent = d.artist || d.album || 'Bilinmiyor';
      if(d.has_cover){
        const h = d.title + '|' + d.artist + '|' + d.album;
        if(h !== lastCoverHash){ lastCoverHash = h; img.src = '/cover?t=' + Date.now(); }
        img.style.display = 'block'; if(ph) ph.style.display = 'none';
      } else { img.style.display = 'none'; if(ph) ph.style.display = 'block'; lastCoverHash = ''; }
    } else { npCard.classList.add('hidden'); }
  }catch(e){}
}
setInterval(updateNP, 2500); updateNP();
async function updateStats(){
  try{
    const r = await fetch('/stats', {cache:'no-store'});
    const d = await r.json();
    document.getElementById('cpu-fill').style.width = d.cpu + '%';
    document.getElementById('cpu-val').textContent = d.cpu.toFixed(0) + '%';
    document.getElementById('ram-fill').style.width = d.ram + '%';
    document.getElementById('ram-val').textContent = d.ram.toFixed(0) + '%';
  }catch(e){}
}
setInterval(updateStats, 2000); updateStats();
</script></body></html>"""


class AnimatedWeatherPanel:
    def __init__(self, parent, forecast_data, city, style, bar_y, bar_height):
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.configure(bg=style["bg"]); self.window.withdraw()
        self.style = style; self.city = city; self.forecast = forecast_data
        self.cards = []; self.bar_y = bar_y; self.bar_height = bar_height
        self.card_height = 60; self.card_spacing = 5
        self.panel_width = 380
        self.panel_height = 15 + 30 + 5 + len(forecast_data) * (self.card_height + self.card_spacing) + 60
        sh = self.window.winfo_screenheight()
        self.open_down = (bar_y + bar_height / 2) < (sh / 2)
        ty = bar_y + bar_height + 5 if self.open_down else bar_y - self.panel_height - 5
        tx = parent.winfo_x() + 100
        self.window.geometry(f"{self.panel_width}x{self.panel_height}+{tx}+{ty}")
        self.build_ui(); self.animate_open()

    def build_ui(self):
        header = tk.Frame(self.window, bg=self.style["bg"])
        header.pack(fill=tk.X, padx=15, pady=(15, 5))
        Label(header, text=f"📍 {self.city}", fg=self.style["fg_main"], bg=self.style["bg"],
              font=("Segoe UI", 14, "bold")).pack(anchor=tk.W)
        ttk.Separator(self.window, orient='horizontal').pack(fill=tk.X, padx=15, pady=5)
        cf = tk.Frame(self.window, bg=self.style["bg"])
        cf.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 10))
        for i, day in enumerate(self.forecast):
            card = tk.Frame(cf, bg=self.style["bar_bg"], relief=tk.FLAT, bd=0)
            card.place(x=0, y=len(self.forecast) * (self.card_height + self.card_spacing),
                       width=350, height=self.card_height)
            Label(card, text=day['date'], fg=self.style["fg_text"], bg=self.style["bar_bg"],
                  font=("Segoe UI", 10)).place(x=10, y=8)
            Label(card, text=day['icon'], fg=self.style["fg_secondary"], bg=self.style["bar_bg"],
                  font=("Segoe UI", 22)).place(x=120, y=5)
            Label(card, text=f"{day['min_temp']}° / {day['max_temp']}°",
                  fg=self.style["fg_clock"], bg=self.style["bar_bg"],
                  font=("Segoe UI", 11, "bold")).place(x=170, y=12)
            Label(card, text=day.get('description', ''), fg=self.style["fg_text"],
                  bg=self.style["bar_bg"], font=("Segoe UI", 8)).place(x=170, y=35)
            self.cards.append(card)
        tk.Button(self.window, text="Kapat", command=self.close,
                  bg=self.style["button_bg"], fg=self.style["fg_text"], bd=0,
                  font=("Segoe UI", 10), padx=15, pady=5, cursor="hand2").pack(pady=(5, 15))

    def animate_open(self):
        self.window.deiconify()
        for i, card in enumerate(self.cards):
            ty = i * (self.card_height + self.card_spacing)
            sy = -self.card_height if self.open_down else len(self.cards) * (self.card_height + self.card_spacing)
            self._animate(card, sy, ty, i * 80)

    def _animate(self, card, sy, ey, delay=0, steps=12):
        if delay > 0:
            self.window.after(delay, lambda: self._animate(card, sy, ey, 0, steps)); return
        step = (ey - sy) / steps; cy = sy
        def mv():
            nonlocal cy
            if abs(cy - ey) < abs(step): card.place(y=ey)
            else:
                cy += step; card.place(y=int(cy)); self.window.after(8, mv)
        mv()

    def close(self):
        try: self.window.destroy()
        except Exception: pass


class AnimatedTaskManager:
    def __init__(self, parent, bg, fg, button_bg, bar_y, bar_height):
        self.parent = parent
        self.win = Toplevel(parent)
        self.win.title("Görev Yöneticisi Lite")
        self.win.configure(bg=bg); self.win.attributes('-topmost', True); self.win.withdraw()
        self.bg = bg; self.fg = fg; self.button_bg = button_bg
        win_w, win_h = 400, 350
        sw = self.win.winfo_screenwidth(); sh = self.win.winfo_screenheight()
        self.target_x = (sw - win_w) // 2
        ty = bar_y + bar_height + 5 if (bar_y + bar_height / 2) < (sh / 2) else bar_y - win_h - 5
        self.target_y = ty; self.start_x = sw
        self.win.geometry(f"{win_w}x{win_h}+{self.start_x}+{ty}")
        frame = tk.Frame(self.win, bg=bg); frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        cols = ("name", "cpu", "memory")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        self.tree.heading("name", text="İşlem Adı"); self.tree.heading("cpu", text="CPU %"); self.tree.heading("memory", text="Bellek (MB)")
        self.tree.column("name", width=200); self.tree.column("cpu", width=80, anchor=tk.CENTER); self.tree.column("memory", width=80, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        sb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set); sb.pack(side=tk.RIGHT, fill=tk.Y)
        bf = tk.Frame(self.win, bg=bg); bf.pack(fill=tk.X, padx=10, pady=(0, 10))
        tk.Button(bf, text="Sonlandır", command=self.kill_selected, bg="#FF5252", fg="white",
                  bd=0, padx=15, pady=5, cursor="hand2").pack(side=tk.LEFT)
        tk.Button(bf, text="Yenile", command=self.refresh_list, bg=button_bg, fg=fg,
                  bd=0, padx=15, pady=5, cursor="hand2").pack(side=tk.RIGHT)
        self.win.deiconify(); self.animate_open(); self.refresh_list()

    def animate_open(self):
        steps = 15; ss = (self.start_x - self.target_x) / steps; cx = self.start_x
        def sl():
            nonlocal cx
            if cx <= self.target_x: self.win.geometry(f"400x350+{self.target_x}+{self.target_y}")
            else:
                cx -= ss; self.win.geometry(f"400x350+{int(cx)}+{self.target_y}"); self.win.after(10, sl)
        sl()

    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                pid = p.info['pid']; nm = p.info['name'] or "?"
                cpu = p.info['cpu_percent'] or 0.0
                mem = p.info['memory_info'].rss / (1024*1024) if p.info['memory_info'] else 0.0
                self.tree.insert("", tk.END, values=(nm, f"{cpu:.1f}", f"{mem:.1f}"), tags=(pid,))
            except (psutil.NoSuchProcess, psutil.AccessDenied): continue
        self.win.after(3000, self.refresh_list)

    def kill_selected(self):
        s = self.tree.selection()
        if s:
            item = self.tree.item(s[0]); pid = item['tags'][0]
            try:
                p = psutil.Process(pid); p.terminate(); self.tree.delete(s[0])
                self.parent.show_notification("Görev Yöneticisi", f"{p.name()} sonlandırıldı.")
            except Exception as e: messagebox.showerror("Hata", f"{e}")


class NexusBar:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Nexus Bar")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)

        self.always_on_top = True
        self.window_locked = False
        self.big_clock = None
        self.web_server = None; self.web_server_running = False
        self.control_server = None; self.control_server_running = False
        self.qr_window = None
        self.music_process = None
        self._media_cache = {"data": None, "time": 0.0}
        self.pomodoro_active = False
        self.water_reminder_active = False

        self._answer_cache = {}
        self.custom_qa = self.load_qa()
        self._groq_working_model = None

        self.current_user = os.getlogin()
        self.settings = self.load_settings()
        if not self.settings.get("groq_api_key"):
            self.settings["groq_api_key"] = GROQ_API_KEY
            self.save_settings()

        self.profile_image_path = self.settings.get("profile_image_path", None)
        self.user_image = self.load_profile_image()
        self.clock_24h = self.settings.get("clock_24h", True)
        self.show_date = self.settings.get("show_date", False)
        self.assistant_enabled = self.settings.get("assistant_enabled", True)
        self.assistant_running = False
        self.assistant_thread = None
        self.listening = False
        self.cloud_offset = 0
        self.processing_command = False

        self.speak_queue = []
        self.speak_condition = threading.Condition()
        self.speak_thread = threading.Thread(target=self._speak_worker, daemon=True)
        self.speak_thread.start()

        self.themes = {
            "Koyu": {"bg": "#1C1C2E", "fg_main": "#4FC3F7", "fg_secondary": "#CE93D8",
                     "fg_warning": "#FFB74D", "fg_text": "#B0B0C0", "fg_clock": "#ECEFF1",
                     "bar_bg": "#2A2A40", "button_bg": "#2A2A40", "flash": "#00FFF0", "alpha": 0.9},
            "Açık": {"bg": "#F5F5F5", "fg_main": "#0288D1", "fg_secondary": "#7B1FA2",
                     "fg_warning": "#E65100", "fg_text": "#424242", "fg_clock": "#212121",
                     "bar_bg": "#E0E0E0", "button_bg": "#E0E0E0", "flash": "#FFD700", "alpha": 0.9},
            "Neon": {"bg": "#0D0221", "fg_main": "#FF007F", "fg_secondary": "#00F0FF",
                     "fg_warning": "#FFEA00", "fg_text": "#FFFFFF", "fg_clock": "#FF00FF",
                     "bar_bg": "#1A1A3E", "button_bg": "#1A1A3E", "flash": "#FFFFFF", "alpha": 0.9},
            "Şeffaf": {"bg": "#000000", "fg_main": "#80D8FF", "fg_secondary": "#B388FF",
                       "fg_warning": "#FFD180", "fg_text": "#CCCCCC", "fg_clock": "#FFFFFF",
                       "bar_bg": "#333333", "button_bg": "#333333", "flash": "#FFFFFF", "alpha": 0.5},
        }
        self.current_theme = self.settings.get("theme", "Koyu")
        self.style = self.themes[self.current_theme]; self.bg = self.style["bg"]
        self.root.configure(bg=self.bg)
        self.root.attributes('-alpha', self.style.get("alpha", 0.9))

        self.main_frame = tk.Frame(self.root, bg=self.bg)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=4)

        self.font_label = ("Segoe UI", 9)
        self.font_value = ("Segoe UI", 10, "bold")
        self.font_small = ("Segoe UI", 8)
        self.font_weather = ("Segoe UI", 12)

        self.last_net_io = psutil.net_io_counters(); self.last_net_time = time.time()
        self._create_widgets()

        self.root.update_idletasks()
        self.root.geometry(f"+{(self.root.winfo_screenwidth()-self.root.winfo_width())//2}+{self.root.winfo_screenheight()-self.root.winfo_height()-30}")
        self.root.bind("<Enter>", lambda e: self.root.attributes('-alpha', self.style.get("alpha", 0.9) + 0.1))
        self.root.bind("<Leave>", lambda e: self.root.attributes('-alpha', self.style.get("alpha", 0.9)))
        self.main_frame.bind("<Button-1>", self.start_move)
        self.main_frame.bind("<ButtonRelease-1>", self.stop_move)
        self.main_frame.bind("<B1-Motion>", self.on_motion)

        self.snap_margin = 20; self.last_collision_time = 0; self.collision_cooldown = 0.5
        self.build_context_menu()
        self.main_frame.bind("<Button-3>", self.show_menu)

        self.city = "Istanbul"; self.lat = 41.0082; self.lon = 28.9784
        self.weather_cache = {}; self.online = False
        self.tray_icon = None
        self.create_tray_icon()
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.register_hotkey()

        self.fetch_location_and_weather()
        self.update_brightness_display()
        threading.Thread(target=self.weather_scheduler, daemon=True).start()
        threading.Thread(target=self.internet_checker, daemon=True).start()
        threading.Thread(target=self.check_for_updates_background, daemon=True).start()

        if PYGAME_AVAILABLE: pygame.mixer.init()
        self.show_welcome_splash()

        if self.assistant_enabled and ASSISTANT_AVAILABLE and EDGE_TTS_AVAILABLE:
            self.root.after(500, self.start_assistant)
        else:
            self.mic_btn.config(text="🔇"); self.update_status_dot()

        self.update_system_info(); self.animate_clouds()

    # ============================================================
    # 🧠 GROQ AI
    # ============================================================
    def get_groq_key(self):
        k = self.settings.get("groq_api_key", "").strip()
        return k or GROQ_API_KEY

    def ask_groq(self, question):
        api_key = self.get_groq_key()
        if not api_key or not api_key.startswith("gsk_"):
            print("[Groq] ⚠️ API anahtarı yok veya geçersiz")
            return None
        models_to_try = []
        if self._groq_working_model:
            models_to_try.append(self._groq_working_model)
        for m in GROQ_MODELS:
            if m != self._groq_working_model:
                models_to_try.append(m)
        for model in models_to_try:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system",
                         "content": "Sen Ahmet adlı Türkçe konuşan bir sesli asistansın. "
                                    "Kısa, net ve doğal Türkçe cevap ver. En fazla 3 cümle."},
                        {"role": "user", "content": question}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 300,
                }
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(url, data=data,
                    headers={"Authorization": f"Bearer {api_key}",
                             "Content-Type": "application/json",
                             "User-Agent": "NexusBar/1.0"},
                    method="POST")
                with urllib.request.urlopen(req, timeout=25) as r:
                    result = json.loads(r.read().decode())
                    choices = result.get("choices", [])
                    if choices:
                        content = choices[0].get("message", {}).get("content", "").strip()
                        if content:
                            print(f"[OK] Groq ({model})")
                            self._groq_working_model = model
                            return content
            except urllib.error.HTTPError as e:
                print(f"[Groq] {model} → HTTP {e.code}")
                if e.code == 401:
                    self.root.after(0, lambda: self.show_notification(
                        "⚠️ Groq", "API anahtarı geçersiz", duration=6000))
                    return None
                elif e.code == 429:
                    self.root.after(0, lambda: self.show_notification(
                        "⚠️ Groq", "Kota aşıldı, biraz bekleyin", duration=6000))
                    return None
                continue
            except Exception as e:
                print(f"[Groq] {model} → {e}")
                continue
        print("[Groq] ❌ Tüm modeller başarısız")
        return None

    def test_groq(self):
        def worker():
            self.show_notification("Groq Test", "🧠 Test ediliyor...", duration=2000)
            if not self.get_groq_key() or not self.get_groq_key().startswith("gsk_"):
                self.root.after(0, lambda: messagebox.showerror(
                    "❌ Groq API Anahtarı Yok",
                    "Kodun üstündeki GROQ_API_KEY satırına anahtarı yapıştır.\n\n"
                    "Ücretsiz: console.groq.com/keys"))
                return
            result = self.ask_groq("Merhaba, kısaca Türkçe kendini tanıt")
            if result:
                self.speak("Yapay zeka çalışıyor", add_sir=True)
                self.root.after(0, lambda: messagebox.showinfo(
                    "🧠 Groq Çalışıyor ✅",
                    f"Kullanılan model: {self._groq_working_model}\n\nYanıt:\n{result[:500]}"))
            else:
                self.root.after(0, lambda: messagebox.showerror(
                    "❌ Groq Çalışmıyor",
                    "Konsola bak — hangi modelin çalıştığını gösterir."))
        threading.Thread(target=worker, daemon=True).start()

    def set_groq_key_dialog(self):
        current = self.get_groq_key()
        key = simpledialog.askstring("Groq API Anahtarı",
            "API anahtarını yapıştır (gsk_... ile başlar):\n\n"
            "Ücretsiz: console.groq.com/keys",
            initialvalue=current, parent=self.root)
        if key is not None:
            key = key.strip()
            self.settings["groq_api_key"] = key
            self._groq_working_model = None
            self.save_settings()
            if key:
                self.show_notification("Groq", "✅ Anahtar kaydedildi")
                self.speak("Groq yapay zekası aktif", add_sir=True)
            else:
                self.show_notification("Groq", "❌ Anahtar silindi")

    # ============================================================
    # AKILLI SORU CEVAPLAMA
    # ============================================================
    def clean_query(self, text):
        q = text.lower().strip()
        q = re.sub(r"[?!.,;:]+", " ", q)
        prefixes = ["ahmet", "hey ahmet", "bana", "lütfen", "söyle", "anlat",
                    "açıkla", "bilgi ver", "nedir", "kimdir", "kim", "ne",
                    "nasıl", "neden", "niçin", "nerede", "ne zaman"]
        suffixes = ["nedir", "kimdir", "ne demek", "ne anlama gelir",
                    "hakkında bilgi ver", "hakkında bilgi", "anlat",
                    "açıkla", "söyle", "ne işe yarar", "ne zaman",
                    "nerede", "nerededir", "nasıldır", "kaçtır", "kaç"]
        for p in sorted(prefixes, key=len, reverse=True):
            if q.startswith(p + " "):
                q = q[len(p)+1:]; break
        for s in sorted(suffixes, key=len, reverse=True):
            if q.endswith(" " + s) or q == s:
                q = q[:-(len(s)+1)] if q != s else ""; break
        q = re.sub(r"\s+", " ", q).strip()
        return q

    def wiki_summary(self, title, lang="tr"):
        try:
            url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
            req = urllib.request.Request(url, headers={"User-Agent": "NexusBar/1.0"})
            with urllib.request.urlopen(req, timeout=7) as r:
                data = json.loads(r.read().decode())
                extract = data.get("extract", "").strip()
                if extract and len(extract) > 30:
                    sentences = re.split(r"(?<=[.!?])\s+", extract)
                    txt = " ".join(sentences[:3])
                    if len(txt) > 500:
                        cut = txt[:500].rfind(".")
                        txt = txt[:cut+1] if cut > 200 else txt[:500] + "..."
                    return txt
        except urllib.error.HTTPError as e:
            if e.code == 404: print(f"[Wiki {lang}] sayfa yok")
            else: print(f"[Wiki {lang}] HTTP {e.code}")
        except Exception as e: print(f"[Wiki {lang}] {e}")
        return None

    def wiki_search(self, query, lang="tr"):
        try:
            search_url = (f"https://{lang}.wikipedia.org/w/api.php?"
                          f"action=opensearch&search={urllib.parse.quote(query)}"
                          f"&limit=1&format=json&namespace=0")
            req = urllib.request.Request(search_url, headers={"User-Agent": "NexusBar/1.0"})
            with urllib.request.urlopen(req, timeout=7) as r:
                data = json.loads(r.read().decode())
                if len(data) >= 2 and data[1]:
                    return self.wiki_summary(data[1][0], lang)
        except Exception as e: print(f"[Wiki search {lang}] {e}")
        return None

    def duckduckgo_answer(self, query):
        try:
            url = ("https://api.duckduckgo.com/?q=" + urllib.parse.quote(query) +
                   "&format=json&no_html=1&skip_disambig=1&kl=tr-tr")
            req = urllib.request.Request(url, headers={"User-Agent": "NexusBar/1.0"})
            with urllib.request.urlopen(req, timeout=7) as r:
                data = json.loads(r.read().decode())
                abstract = data.get("AbstractText", "").strip()
                if abstract and len(abstract) > 30: return abstract
                definition = data.get("Definition", "").strip()
                if definition and len(definition) > 20: return definition
                answer = data.get("Answer", "").strip()
                if answer: return str(answer)
        except Exception as e: print(f"DDG: {e}")
        return None

    def translate_to_en(self, text):
        try:
            url = ("https://translate.googleapis.com/translate_a/single?"
                   f"client=gtx&sl=tr&tl=en&dt=t&q={urllib.parse.quote(text)}")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as r:
                data = json.loads(r.read().decode())
                if data and data[0]:
                    return "".join(seg[0] for seg in data[0] if seg and seg[0])
        except Exception as e: print(f"Translate: {e}")
        return None

    def ask_anything(self, question, speak_answer=True):
        if not question or len(question.strip()) < 2:
            msg = "Ne sormak istediğinizi anlayamadım"
            if speak_answer: self.speak(msg, add_sir=True)
            return msg
        key = question.lower().strip()
        if key in self._answer_cache:
            ans = self._answer_cache[key]
            if speak_answer: self.speak(ans, add_sir=True)
            return ans
        query = self.clean_query(question)
        if not query or len(query) < 2: query = question.strip()
        print(f"[SORU] '{question}' → temiz: '{query}'")
        answer = self.wiki_summary(query, "tr")
        if answer:
            print("[OK] Wikipedia TR direkt"); self._answer_cache[key] = answer
            if speak_answer: self.speak(answer, add_sir=True)
            return answer
        answer = self.wiki_search(query, "tr")
        if answer:
            print("[OK] Wikipedia TR arama"); self._answer_cache[key] = answer
            if speak_answer: self.speak(answer, add_sir=True)
            return answer
        answer = self.duckduckgo_answer(query)
        if answer:
            print("[OK] DuckDuckGo"); self._answer_cache[key] = answer
            if speak_answer: self.speak(answer, add_sir=True)
            return answer
        print("[..] Groq AI'ya soruyorum...")
        answer = self.ask_groq(question)
        if answer:
            self._answer_cache[key] = answer
            if speak_answer: self.speak(answer, add_sir=True)
            return answer
        try:
            en_query = self.translate_to_en(query) or query
            answer = self.wiki_summary(en_query, "en") or self.wiki_search(en_query, "en")
            if answer:
                print("[OK] Wikipedia EN")
                msg = f"İngilizce kaynaktan: {answer}"
                self._answer_cache[key] = msg
                if speak_answer: self.speak(msg, add_sir=True)
                return msg
        except Exception as e: print(f"[Wiki EN] atlandı: {e}")
        msg = f"'{query}' hakkında net bir bilgi bulamadım. Google'da arıyorum."
        try: webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
        except Exception: pass
        self._answer_cache[key] = msg
        if speak_answer: self.speak(msg, add_sir=True)
        return msg

    def is_question(self, command):
        c = command.lower().strip()
        q_words = ["nedir", "kimdir", "ne demek", "ne zaman", "nerede",
                   "nasıl", "neden", "niçin", "kaç", "hakkında",
                   "anlat", "açıkla", "söyle", "bilgi ver", "ne işe yarar"]
        if any(w in c for w in q_words): return True
        if re.search(r"\b(mi|mı|mu|mü)\b", c): return True
        if c.endswith("?"): return True
        return False

    # ============================================================
    # BİLGİ BANKASI
    # ============================================================
    def load_qa(self):
        if os.path.exists(QA_FILE):
            try:
                with open(QA_FILE, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    if isinstance(d, dict): return d
            except Exception: pass
        return {}

    def save_qa(self):
        try:
            with open(QA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.custom_qa, f, ensure_ascii=False, indent=2)
        except Exception: pass

    def lookup_qa(self, question):
        if not hasattr(self, 'custom_qa') or not self.custom_qa: return None
        q = self.clean_query(question).lower()
        if not q: return None
        if q in self.custom_qa: return self.custom_qa[q]
        for k, v in self.custom_qa.items():
            if k in q or q in k: return v
        return None

    # ============================================================
    # HESAP / DÖVİZ / HABER
    # ============================================================
    def calculate(self, text):
        t = text.lower()
        reps = {"artı":"+", "topla":"+", "eksi":"-", "çıkar":"-",
                "çarpı":"*", "kere":"*", "çarp":"*", "bölü":"/", "böl":"/",
                "üzeri":"**", "kuvvet":"**", "virgül":".", "nokta":".",
                "kaç":"", "eder":"", "kaçtır":"", "sonucu":"", "nedir":"",
                "hesapla":"", "yapar":""}
        for k, v in reps.items(): t = t.replace(k, v)
        safe = re.sub(r"[^0-9+\-*/().\s]", "", t)
        if not safe.strip(): return None
        try:
            r = eval(safe, {"__builtins__": {}}, {})
            if isinstance(r, (int, float)):
                return int(r) if r == int(r) else round(r, 4)
        except Exception: pass
        return None

    def get_exchange_rate(self, currency):
        code_map = {"dolar":"USD","euro":"EUR","sterlin":"GBP","frank":"CHF","yen":"JPY","ruble":"RUB"}
        base = code_map.get(currency.lower(), currency.upper()[:3])
        try:
            url = f"https://api.frankfurter.app/latest?from={base}&to=TRY"
            req = urllib.request.Request(url, headers={"User-Agent": "NexusBar/1.0"})
            with urllib.request.urlopen(req, timeout=5) as r:
                data = json.loads(r.read().decode())
                rate = data.get("rates", {}).get("TRY")
                if rate: return {"code": base, "rate": rate, "date": data.get("date", "")}
        except Exception as e: print("Döviz:", e)
        return None

    def read_news(self, count=3):
        feeds = ["https://www.trthaber.com/sondakika_articles.rss",
                 "https://www.aa.com.tr/tr/rss/default?cat=guncel"]
        for url in feeds:
            try:
                req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=6) as r: xml_data = r.read()
                root = ET.fromstring(xml_data)
                items = root.findall(".//item")[:count]
                news = [i.find("title").text.strip() for i in items if i.find("title") is not None and i.find("title").text]
                if news: return news
            except Exception as e: print(f"RSS: {e}")
        return []

    # ============================================================
    # POMODORO / SU / OTOMATİK BAŞLAT
    # ============================================================
    def start_pomodoro(self, minutes=25):
        if self.pomodoro_active:
            self.show_notification("Pomodoro", "Zaten aktif — iptal")
            self.pomodoro_active = False; return
        self.pomodoro_active = True
        self.show_notification("Pomodoro", f"🍅 {minutes} dakika başladı")
        self.speak(f"{minutes} dakikalık pomodoro başlatıldı", add_sir=True)
        def w():
            time.sleep(minutes * 60)
            if not self.pomodoro_active: return
            self.pomodoro_active = False
            self.root.after(0, lambda: self.show_notification("Pomodoro", f"⏰ {minutes} dakika doldu!"))
            self.speak("Pomodoro süresi doldu. Mola zamanı", add_sir=True)
            try:
                for _ in range(3):
                    winsound.Beep(1000, 300); winsound.Beep(1500, 300)
            except Exception: pass
        threading.Thread(target=w, daemon=True).start()

    def toggle_water_reminder(self):
        if self.water_reminder_active:
            self.water_reminder_active = False
            self.show_notification("💧 Su", "Kapatıldı")
        else:
            self.water_reminder_active = True
            self.show_notification("💧 Su", "Her saat hatırlatacak")
            threading.Thread(target=self._water_worker, daemon=True).start()

    def _water_worker(self):
        while self.water_reminder_active:
            time.sleep(3600)
            if not self.water_reminder_active: break
            self.root.after(0, lambda: self.show_notification("💧 Su", "Bir bardak su içme zamanı!"))
            self.speak("Bir bardak su içmeyi unutmayın", add_sir=True)

    def is_autostart_enabled(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, "NexusBar"); winreg.CloseKey(key); return True
            except FileNotFoundError:
                winreg.CloseKey(key); return False
        except Exception: return False

    def toggle_autostart(self):
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        script_path = os.path.abspath(__file__)
        python_exe = sys.executable.replace("python.exe", "pythonw.exe")
        if not os.path.exists(python_exe): python_exe = sys.executable
        cmd = f'"{python_exe}" "{script_path}"'
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            if self.is_autostart_enabled():
                winreg.DeleteValue(key, "NexusBar")
                self.show_notification("Otomatik Başlatma", "❌ Kapatıldı")
            else:
                winreg.SetValueEx(key, "NexusBar", 0, winreg.REG_SZ, cmd)
                self.show_notification("Otomatik Başlatma", "✅ Açıldı")
            winreg.CloseKey(key); self.build_context_menu()
        except Exception as e:
            messagebox.showerror("Hata", f"{e}")

    # ============================================================
    # KARŞILAMA
    # ============================================================
    def show_welcome_splash(self):
        s = Toplevel(self.root); s.overrideredirect(True); s.attributes('-topmost', True)
        s.configure(bg=self.bg)
        s.geometry("360x110+{}+{}".format((self.root.winfo_screenwidth()-360)//2,
                                          (self.root.winfo_screenheight()-110)//2))
        Label(s, text="🦁 Nexus Bar", fg=self.style["fg_clock"], bg=self.bg,
              font=("Segoe UI", 16, "bold")).pack(pady=(10,0))
        Label(s, text=f"{ASSISTANT_NAME} hazır — her soruyu sorabilirsin!",
              fg=self.style["fg_text"], bg=self.bg, font=("Segoe UI", 11)).pack()
        s.after(3200, s.destroy)

    # ============================================================
    # PROFİL
    # ============================================================
    def create_circular_image(self, image_path, size):
        try:
            img = Image.open(image_path).convert("RGBA").resize((size, size), Image.LANCZOS)
            mask = Image.new("L", (size, size), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
            r = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            r.paste(img, (0, 0), mask); return ImageTk.PhotoImage(r)
        except Exception: return None

    def load_profile_image(self):
        if self.profile_image_path and os.path.exists(self.profile_image_path):
            img = self.create_circular_image(self.profile_image_path, 24)
            if img: return img
        try:
            u = os.getlogin()
            for d in [os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'AccountPictures'),
                      os.path.join('C:', 'Users', u, 'AppData', 'Roaming', 'Microsoft', 'Windows', 'AccountPictures'),
                      os.path.join('C:', 'ProgramData', 'Microsoft', 'User Account Pictures')]:
                if os.path.exists(d):
                    files = glob.glob(os.path.join(d, '*.jpg')) + glob.glob(os.path.join(d, '*.png'))
                    if files:
                        img = self.create_circular_image(max(files, key=os.path.getmtime), 24)
                        if img: return img
        except Exception: pass
        return None

    def choose_profile_image(self):
        fp = filedialog.askopenfilename(title="Profil Fotoğrafı Seç",
            filetypes=[("Resim dosyaları", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if not fp: return
        try:
            dest = os.path.join(os.path.dirname(SETTINGS_FILE), "profile_image.png")
            img = Image.open(fp).convert("RGBA"); img.thumbnail((256, 256)); img.save(dest, "PNG")
            self.profile_image_path = dest
            self.user_image = self.create_circular_image(dest, 24)
            self.save_settings(); self.update_profile_button()
            self.show_notification("Profil", "Güncellendi.")
        except Exception as e: messagebox.showerror("Hata", f"{e}")

    def update_profile_button(self):
        if self.user_image: self.profile_btn.config(image=self.user_image, text="")
        else: self.profile_btn.config(image="", text="👤")

    # ============================================================
    # TTS
    # ============================================================
    def speak(self, text, add_sir=False):
        if not text: return
        if add_sir: text += " efendim"
        with self.speak_condition:
            self.speak_queue.append(text); self.speak_condition.notify()

    def _speak_worker(self):
        while True:
            with self.speak_condition:
                while not self.speak_queue: self.speak_condition.wait()
                text = self.speak_queue.pop(0)
            if not EDGE_TTS_AVAILABLE: continue
            try:
                async def _edge():
                    c = edge_tts.Communicate(text, ASSISTANT_VOICE_NAME)
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                        tf = fp.name
                    await c.save(tf)
                    if PYGAME_AVAILABLE:
                        pygame.mixer.music.load(tf); pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy(): time.sleep(0.1)
                        pygame.mixer.music.stop(); pygame.mixer.music.unload()
                    try: os.unlink(tf)
                    except Exception: pass
                asyncio.run(_edge())
            except Exception as e: print("TTS:", e)

    # ============================================================
    # SES
    # ============================================================
    def set_volume_percent(self, percent):
        if not PYCAW_AVAILABLE: return False
        try:
            d = AudioUtilities.GetSpeakers()
            i = d.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            v = cast(i, POINTER(IAudioEndpointVolume))
            v.SetMasterVolumeLevelScalar(percent / 100.0, None); return True
        except Exception: return False

    def get_volume_percent(self):
        if not PYCAW_AVAILABLE: return None
        try:
            d = AudioUtilities.GetSpeakers()
            i = d.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            v = cast(i, POINTER(IAudioEndpointVolume))
            return round(v.GetMasterVolumeLevelScalar() * 100)
        except Exception: return None

    # ============================================================
    # MEDYA
    # ============================================================
    def media_play_pause(self):
        VK = 0xB3; ctypes.windll.user32.keybd_event(VK, 0, 0, 0); ctypes.windll.user32.keybd_event(VK, 0, 2, 0)
    def media_next(self):
        VK = 0xB0; ctypes.windll.user32.keybd_event(VK, 0, 0, 0); ctypes.windll.user32.keybd_event(VK, 0, 2, 0)
    def media_prev(self):
        VK = 0xB1; ctypes.windll.user32.keybd_event(VK, 0, 0, 0); ctypes.windll.user32.keybd_event(VK, 0, 2, 0)
    def volume_up(self):
        VK = 0xAF; ctypes.windll.user32.keybd_event(VK, 0, 0, 0); ctypes.windll.user32.keybd_event(VK, 0, 2, 0)
    def volume_down(self):
        VK = 0xAE; ctypes.windll.user32.keybd_event(VK, 0, 0, 0); ctypes.windll.user32.keybd_event(VK, 0, 2, 0)
    def volume_mute(self):
        VK = 0xAD; ctypes.windll.user32.keybd_event(VK, 0, 0, 0); ctypes.windll.user32.keybd_event(VK, 0, 2, 0)

    async def _fetch_media_async(self):
        if not MEDIA_AVAILABLE: return None
        try:
            m = await MediaManager.request_async()
            s = m.get_current_session()
            if not s: return None
            try:
                pb = s.get_playback_info()
                if pb.playback_status in (0, 3): return None
            except Exception: pass
            props = await s.try_get_media_properties_async()
            if not props: return None
            title = props.title or ""; artist = props.artist or ""; album = props.album_title or ""
            cb = None
            if props.thumbnail:
                try:
                    st = await props.thumbnail.open_read_async()
                    if st:
                        sz = st.size
                        if sz > 0:
                            buf = Buffer(sz)
                            await st.read_async(buf, sz, InputStreamOptions.READ_AHEAD)
                            rd = DataReader.from_buffer(buf); data = bytearray(sz); rd.read_bytes(data)
                            cb = bytes(data)
                        st.close()
                except Exception: pass
            return {"title": title, "artist": artist, "album": album, "cover_bytes": cb}
        except Exception: return None

    def get_now_playing(self):
        n = time.time()
        if n - self._media_cache["time"] < 1.5: return self._media_cache["data"]
        try: r = asyncio.run(self._fetch_media_async())
        except Exception: r = None
        self._media_cache["data"] = r; self._media_cache["time"] = n; return r

    def get_cover_bytes(self):
        i = self.get_now_playing()
        return i.get("cover_bytes") if i else None

    def open_music_app(self):
        if self.music_process and self.music_process.poll() is None:
            self.show_notification("Müzik", "Zaten açık."); return
        try: os.startfile("spotify:"); self.show_notification("Müzik", "Spotify 🎵"); return
        except Exception: pass
        try:
            self.music_process = subprocess.Popen("wmplayer.exe"); self.show_notification("Müzik", "WMP 🎵"); return
        except Exception: pass
        try: os.startfile(os.path.join(os.environ["USERPROFILE"], "Music"))
        except Exception as e: self.show_notification("Müzik", f"{e}")

    def close_music_app(self):
        closed = []
        if self.music_process and self.music_process.poll() is None:
            try: self.music_process.terminate(); closed.append("Müzik"); self.music_process = None
            except Exception: pass
        for p in psutil.process_iter(['pid', 'name']):
            try:
                nm = (p.info['name'] or "").lower()
                if nm in ["spotify.exe", "wmplayer.exe", "musicbee.exe", "aimp.exe"]:
                    p.terminate(); closed.append(nm.replace(".exe","").title())
            except Exception: continue
        if closed: self.show_notification("Müzik", f"Kapatıldı: {', '.join(set(closed))}")
        else: self.show_notification("Müzik", "Açık uygulama yok.")

    # ============================================================
    # DURUM DAİRESİ
    # ============================================================
    def update_status_dot(self):
        c = "#4FC3F7" if self.listening else "#69F0AE" if self.assistant_running else "#FF5252"
        if hasattr(self, 'status_canvas'):
            self.status_canvas.itemconfig(self.status_dot, fill=c)
            self.status_canvas.itemconfig(self.outer_circle, outline=c)

    def animate_clouds(self):
        if hasattr(self, 'status_canvas'):
            self.cloud_offset = (self.cloud_offset + 1) % 20
            a = math.radians(self.cloud_offset * 18); r = 8; cx, cy = 20, 20
            x1 = cx + r * math.cos(a) - 5; y1 = cy + r * math.sin(a) - 5
            self.status_canvas.coords(self.cloud1, x1, y1, x1+10, y1+8)
            a2 = math.radians(self.cloud_offset * 18 + 120)
            x3 = cx + r * math.cos(a2) - 5; y3 = cy + r * math.sin(a2) - 5
            self.status_canvas.coords(self.cloud2, x3, y3, x3+10, y3+8)
            a3 = math.radians(self.cloud_offset * 18 + 240)
            x4 = cx + r * math.cos(a3) - 5; y4 = cy + r * math.sin(a3) - 5
            self.status_canvas.coords(self.cloud3, x4, y4, x4+10, y4+8)
        self.root.after(50, self.animate_clouds)

    # ============================================================
    # ASİSTAN
    # ============================================================
    def start_assistant(self):
        if self.assistant_running: return
        self.assistant_running = True; self.assistant_enabled = True; self.save_settings()
        self.mic_btn.config(text="🎤"); self.update_status_dot()
        self.assistant_thread = threading.Thread(target=self._assistant_loop, daemon=True)
        self.assistant_thread.start()
        self.speak(f"Merhaba {self.current_user}, ben {ASSISTANT_NAME}. Ne sormak istersiniz?")
        self.show_notification(f"{ASSISTANT_NAME}", "Soru sorun, yapay zeka cevaplasın!")

    def stop_assistant(self):
        self.assistant_running = False; self.assistant_enabled = False; self.save_settings()
        self.mic_btn.config(text="🔇"); self.update_status_dot()
        self.show_notification(f"{ASSISTANT_NAME}", "Dinleme durdu.")

    def _assistant_loop(self):
        r = sr.Recognizer(); r.energy_threshold = 300
        r.dynamic_energy_threshold = True; r.pause_threshold = 0.8
        with sr.Microphone() as s: r.adjust_for_ambient_noise(s, duration=1.5)
        while self.assistant_running:
            if self.processing_command: time.sleep(0.1); continue
            try:
                with sr.Microphone() as s:
                    print("🎤 Dinleniyor...")
                    self.listening = True; self.root.after(0, self.update_status_dot)
                    audio = r.listen(s, timeout=5, phrase_time_limit=12)
                    self.listening = False; self.root.after(0, self.update_status_dot)
                try:
                    cmd = r.recognize_google(audio, language="tr-TR").lower()
                    print(f"🗣️ Algılanan: {cmd}")
                    self.processing_command = True
                    self.root.after(0, lambda c=cmd: self._process_command(c))
                except sr.UnknownValueError: print("Anlaşılamadı.")
                except sr.RequestError as e: print("Google:", e); time.sleep(2)
            except sr.WaitTimeoutError: pass
            except Exception as e: print("Hata:", e); time.sleep(1)

    def _process_command(self, command):
        try:
            print(f"⚙️ İşleniyor: {command}")

            # ÖNCE ÖĞRETİLENLER
            custom = self.lookup_qa(command)
            if custom:
                self.speak(custom, add_sir=True)
                self.show_notification("Ahmet", custom[:120])
                self.processing_command = False
                return

            # AI TEST
            if ("yapay zeka" in command or "groq" in command) and ("test" in command or "kontrol" in command):
                self.test_groq()
                self.speak("Yapay zeka test ediliyor", add_sir=True)
                self.processing_command = False
                return

            # GROQ KEY
            if "groq" in command and ("anahtar" in command or "api" in command):
                self.set_groq_key_dialog()
                self.speak("Groq anahtar penceresi açıldı", add_sir=True)
                self.processing_command = False
                return

            # ÖĞRETME
            m = re.match(r"^(?:öğren|ogren)\s+(.+?)\s+(?:cevabı|cevabi|eşittir|esittir|=)\s+(.+)$", command)
            if m:
                q, a = m.group(1).strip(), m.group(2).strip()
                self.custom_qa[self.clean_query(q).lower()] = a
                self.save_qa()
                self.speak("Tamam öğrendim", add_sir=True)
                self.processing_command = False
                return

            # QR
            if any(k in command for k in ["qr kod", "qr kodu", "kare kod", "qr aç", "telefon kontrol", "telefondan kontrol"]):
                self.show_qr_code()
                self.speak("QR kod açılıyor", add_sir=True)
                self.processing_command = False; return

            # MATEMATİK
            if any(k in command for k in ["artı", "eksi", "çarpı", "bölü", "kere", "kaç eder", "kaç yapar"]):
                res = self.calculate(command)
                if res is not None:
                    self.speak(f"Sonuç {res}", add_sir=True)
                    self.show_notification("Hesap", f"= {res}")
                    self.processing_command = False; return

            # DÖVİZ
            if any(k in command for k in ["dolar", "euro", "sterlin", "döviz", "kur"]):
                for cur in ["dolar", "euro", "sterlin"]:
                    if cur in command:
                        info = self.get_exchange_rate(cur)
                        if info:
                            msg = f"{cur.capitalize()} {info['rate']:.2f} lira"
                            self.speak(msg, add_sir=True)
                            self.show_notification("Döviz", f"{info['code']} = {info['rate']:.2f}")
                        self.processing_command = False; return
                self.processing_command = False; return

            # HABER
            if any(k in command for k in ["haber", "gündem", "son dakika"]):
                news = self.read_news(3)
                if news:
                    self.speak("İşte son haberler", add_sir=True)
                    for i, n in enumerate(news, 1): self.speak(f"{i}. {n}", add_sir=True)
                    self.show_notification("Haberler", "\n".join(news))
                self.processing_command = False; return

            # POMODORO
            if any(k in command for k in ["pomodoro", "odaklan"]):
                nums = re.findall(r"\d+", command); minutes = 25
                if nums:
                    try:
                        minutes = int(nums[0])
                        if minutes > 120 or minutes < 1: minutes = 25
                    except Exception: minutes = 25
                self.start_pomodoro(minutes)
                self.processing_command = False; return

            # SU
            if any(k in command for k in ["su iç", "su hatırlat"]):
                self.toggle_water_reminder()
                self.processing_command = False; return

            # OTOMATİK BAŞLAT
            if any(k in command for k in ["otomatik başlat", "bilgisayar açılınca"]):
                self.toggle_autostart()
                self.processing_command = False; return

            # ========================================
            # MÜZİK AÇ / KAPAT (uygulama)
            # ========================================
            if any(k in command for k in ["müzik aç", "müziği aç", "müzik başlat", "müzik oynat"]):
                self.open_music_app(); self.speak("Müzik açılıyor", add_sir=True)
                self.processing_command = False; return
            if any(k in command for k in ["müzik kapat", "müziği kapat", "müzik durdur"]):
                self.close_music_app(); self.speak("Müzik kapatıldı", add_sir=True)
                self.processing_command = False; return

            # ========================================
            # MÜZİK DURAKLAT
            # ========================================
            if any(k in command for k in ["duraklat", "duraklat müziği", "müziği duraklat",
                                           "şarkıyı durdur", "müziği durdur", "durdur"]):
                self.media_play_pause(); self.speak("Duraklatıldı", add_sir=True)
                self.processing_command = False; return

            # ========================================
            # MÜZİK DEVAM ETTİR (çok esnek)
            # ========================================
            if any(k in command for k in ["devam et", "devam ettir", "devam etsene",
                                           "kaldığın yerden", "devam", "müziği devam",
                                           "müzik devam", "çalmaya devam", "oynat",
                                           "yeniden başlat müziği"]):
                self.media_play_pause(); self.speak("Müzik devam ediyor", add_sir=True)
                self.processing_command = False; return

            # SONRAKİ / ÖNCEKİ
            if "sonraki" in command:
                self.media_next(); self.speak("Sonraki", add_sir=True)
                self.processing_command = False; return
            if "önceki" in command:
                self.media_prev(); self.speak("Önceki", add_sir=True)
                self.processing_command = False; return

            # NE ÇALIYOR
            if any(k in command for k in ["ne çalıyor", "hangi şarkı"]):
                info = self.get_now_playing()
                if info and info.get("title"):
                    msg = f"Şu an {info['title']}"
                    if info.get("artist"): msg += f", {info['artist']}"
                    self.speak(msg, add_sir=True)
                else: self.speak("Şu an bir şey çalmıyor", add_sir=True)
                self.processing_command = False; return

            # SES
            if any(k in command for k in ["sesi yüzde", "ses yüzde"]):
                try:
                    p = int(''.join(filter(str.isdigit, command)))
                    if 0 <= p <= 100:
                        if self.set_volume_percent(p): self.speak(f"Ses yüzde {p}", add_sir=True)
                except Exception: pass
                self.processing_command = False; return
            if any(k in command for k in ["ses aç", "sesi yükselt", "ses artır"]):
                self.volume_up(); self.speak("Ses artırıldı", add_sir=True)
                self.processing_command = False; return
            if any(k in command for k in ["ses kıs", "sesi azalt", "ses kız"]):
                self.volume_down(); self.speak("Ses azaltıldı", add_sir=True)
                self.processing_command = False; return
            if "sesi kapat" in command or "sessize al" in command:
                self.volume_mute(); self.speak("Sessiz", add_sir=True)
                self.processing_command = False; return

            # SİSTEM
            if "sistem bilgisi" in command or "bilgisayar durumu" in command:
                cpu = psutil.cpu_percent(interval=0.1); ram = psutil.virtual_memory().percent
                self.speak(f"CPU {cpu:.0f}, RAM {ram:.0f}", add_sir=True)
                self.processing_command = False; return
            if "pil" in command or "şarj" in command:
                b = psutil.sensors_battery()
                if b: self.speak(f"Pil yüzde {b.percent}", add_sir=True)
                self.processing_command = False; return
            if "bugün" in command or "tarih" in command:
                n = datetime.datetime.now()
                self.speak(f"Bugün {n.day} {n.strftime('%B')} {n.year}, {n.strftime('%A')}", add_sir=True)
                self.processing_command = False; return
            if "saat kaç" in command or command == "saat":
                self.speak(f"Saat {datetime.datetime.now().strftime('%H:%M')}", add_sir=True)
                self.processing_command = False; return
            if "hava" in command:
                if self.weather_cache.get("current"):
                    c = self.weather_cache["current"]
                    self.speak(f"{c['description']}, {c['min_temp']} ile {c['max_temp']} derece", add_sir=True)
                self.processing_command = False; return

            # UYGULAMA
            if "not defteri" in command:
                subprocess.Popen("notepad.exe"); self.speak("Not defteri", add_sir=True)
                self.processing_command = False; return
            if "hesap makinesi" in command:
                subprocess.Popen("calc.exe"); self.speak("Hesap makinesi", add_sir=True)
                self.processing_command = False; return
            if "görev yöneticisini" in command:
                self.show_task_manager(); self.speak("Görev yöneticisi", add_sir=True)
                self.processing_command = False; return
            if "tarayıcıyı aç" in command or "interneti aç" in command:
                webbrowser.open("https://www.google.com"); self.speak("Tarayıcı", add_sir=True)
                self.processing_command = False; return
            if "chrome aç" in command:
                subprocess.Popen("chrome.exe"); self.speak("Chrome", add_sir=True)
                self.processing_command = False; return
            if "youtube'da ara" in command or "youtube ara" in command:
                q = command.replace("youtube'da ara", "").replace("youtube ara", "").strip()
                if q:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}")
                    self.speak(f"YouTube'da {q}", add_sir=True)
                self.processing_command = False; return

            # KAPATMA
            if "bilgisayarı kapat" in command:
                if messagebox.askyesno("Onay", "Kapatmak istediğinize emin misiniz?"):
                    os.system("shutdown /s /t 10"); self.speak("Kapanıyor", add_sir=True)
                self.processing_command = False; return
            if "yeniden başlat" in command:
                if messagebox.askyesno("Onay", "Yeniden başlatmak istediğinize emin misiniz?"):
                    os.system("shutdown /r /t 10"); self.speak("Yeniden başlıyor", add_sir=True)
                self.processing_command = False; return

            # ALARM
            if "alarm kur" in command or "zamanlayıcı" in command:
                try:
                    if "dakika" in command:
                        d = int(''.join(filter(str.isdigit, command)))
                        self.speak(f"{d} dakika sonra uyaracağım", add_sir=True)
                        threading.Thread(target=self._alarm_worker, args=(d*60, "Alarm!"), daemon=True).start()
                    elif "saniye" in command:
                        s = int(''.join(filter(str.isdigit, command)))
                        threading.Thread(target=self._alarm_worker, args=(s, "Alarm!"), daemon=True).start()
                except Exception: pass
                self.processing_command = False; return

            if "hatırlat" in command:
                try:
                    d = int(''.join(filter(str.isdigit, command)))
                    m = command.split("sonra")[-1].strip() or "Hatırlatıcı!"
                    self.speak(f"{d} dakika sonra hatırlatacağım", add_sir=True)
                    threading.Thread(target=self._alarm_worker, args=(d*60, m), daemon=True).start()
                except Exception: pass
                self.processing_command = False; return

            # ŞAKA
            if "şaka yap" in command or "fıkra anlat" in command:
                jokes = ["Bir bilgisayar neden denize giremez? Çünkü dalgalardan korkar!",
                         "Neden matematik kitabı üzgündü? Çünkü çok problemi vardı."]
                j = random.choice(jokes); self.speak(j, add_sir=True); self.show_notification("Şaka", j)
                self.processing_command = False; return
            if "iltifat et" in command:
                self.speak(random.choice(["Harika görünüyorsunuz!", "Zekanız beni şaşırtıyor."]), add_sir=True)
                self.processing_command = False; return

            # ÇEŞİTLİ
            if "temizlik" in command or "temizle" in command:
                self.clean_temp_and_recycle(); self.speak("Temizlik", add_sir=True)
                self.processing_command = False; return
            if "ekran görüntüsü" in command or "fotoğraf çek" in command:
                self.take_screenshot(); self.speak("Ekran alındı", add_sir=True)
                self.processing_command = False; return
            if "kilitle" in command:
                self.lock_windows(); self.speak("Kilitleniyor", add_sir=True)
                self.processing_command = False; return
            if "çubuğu gizle" in command or "kaybol" in command:
                self.minimize_to_tray(); self.speak("Gizlendi", add_sir=True)
                self.processing_command = False; return
            if "çubuğu göster" in command or "ortaya çık" in command:
                self.show_window(); self.speak("Burada", add_sir=True)
                self.processing_command = False; return

            # TEŞEKKÜR
            if "teşekkür" in command or command.strip() == "yeter":
                self.speak("Rica ederim, görüşürüz", add_sir=True)
                self.processing_command = False; return

            # AKILLI CEVAP
            print(f"[SORU MODU] '{command}' → akıllı arama")
            self.processing_command = True
            threading.Thread(target=self._search_and_speak, args=(command,), daemon=True).start()

        except Exception as e:
            print("Komut işleme hatası:", e)
            self.processing_command = False

    def _search_and_speak(self, question):
        try:
            answer = self.ask_anything(question, speak_answer=False)
            self.root.after(0, lambda: self.show_notification("Ahmet", answer[:140]))
            self.speak(answer, add_sir=True)
        except Exception as e:
            print("Arama hatası:", e)
            self.speak("Arama sırasında hata oldu", add_sir=True)
        finally:
            self.processing_command = False

    def _alarm_worker(self, sec, msg="Alarm!"):
        time.sleep(sec)
        self.root.after(0, lambda: self.show_notification("Hatırlatıcı", msg))
        self.speak(msg, add_sir=True)

    def lock_windows(self): ctypes.windll.user32.LockWorkStation()

    # ============================================================
    # PROFİL POPUP
    # ============================================================
    def show_profile_popup(self):
        p = Toplevel(self.root); p.overrideredirect(True); p.attributes('-topmost', True)
        p.configure(bg=self.style["bg"])
        p.geometry(f"260x120+{self.root.winfo_x()+10}+{self.root.winfo_y()-110}")
        f = tk.Frame(p, bg=self.style["bg"]); f.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        ar = None
        if self.profile_image_path and os.path.exists(self.profile_image_path):
            ar = self.create_circular_image(self.profile_image_path, 48)
        if ar:
            l = Label(f, image=ar, bg=self.style["bg"]); l.image = ar; l.pack(side=tk.LEFT, padx=(0, 10))
        else:
            Label(f, text="👤", font=("Segoe UI", 24), bg=self.style["bg"], fg=self.style["fg_text"]).pack(side=tk.LEFT, padx=(0, 10))
        i = tk.Frame(f, bg=self.style["bg"]); i.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        Label(i, text=f"👤 {self.current_user}", fg=self.style["fg_clock"], bg=self.style["bg"],
              font=("Segoe UI", 12, "bold")).pack(anchor=tk.W)
        bf = tk.Frame(i, bg=self.style["bg"]); bf.pack(anchor=tk.W, pady=(10, 0))
        def cn():
            nn = simpledialog.askstring("İsim", "Yeni:", initialvalue=self.current_user)
            if nn and nn.strip():
                self.current_user = nn.strip(); self.save_settings(); p.destroy()
                if self.assistant_running:
                    self.stop_assistant(); self.root.after(100, self.start_assistant)
        tk.Button(bf, text="✏️ İsim", command=cn, bg=self.style["button_bg"], fg=self.style["fg_text"],
                  bd=0, padx=8, pady=2, font=("Segoe UI", 8), cursor="hand2").pack(side=tk.LEFT, padx=(0,5))
        tk.Button(bf, text="📷 Foto", command=self.choose_profile_image, bg=self.style["button_bg"],
                  fg=self.style["fg_text"], bd=0, padx=8, pady=2, font=("Segoe UI", 8), cursor="hand2").pack(side=tk.LEFT)
        p.after(8000, p.destroy)

    # ============================================================
    # TELEFON
    # ============================================================
    def _get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]; s.close(); return ip
        except Exception:
            try: return socket.gethostbyname(socket.gethostname())
            except Exception: return "127.0.0.1"

    def _handle_remote_command(self, cmd):
        m = {
            "playpause": self.media_play_pause, "next": self.media_next, "prev": self.media_prev,
            "volup": self.volume_up, "voldown": self.volume_down, "mute": self.volume_mute,
            "screenshot": self.take_screenshot, "clean": self.clean_temp_and_recycle,
            "lock": self.lock_windows, "privacy": self.toggle_privacy, "taskmgr": self.show_task_manager,
            "music": self.open_music_app, "musicclose": self.close_music_app, "assistant": self.toggle_assistant,
            "minimize": self.minimize_to_tray, "show": self.show_window, "quit": self.quit_app,
            "theme_koyu": lambda: self.change_theme("Koyu"),
            "theme_acik": lambda: self.change_theme("Açık"),
            "theme_neon": lambda: self.change_theme("Neon"),
            "theme_seffaf": lambda: self.change_theme("Şeffaf"),
            "pomodoro": lambda: self.start_pomodoro(25),
            "water": self.toggle_water_reminder,
        }
        f = m.get(cmd)
        if f: self.root.after(0, f)

    def start_control_server(self):
        if self.control_server_running: self.show_qr_code(); return
        parent = self
        html_bytes = CONTROL_HTML.replace("__VERSION__", CURRENT_VERSION).encode("utf-8")

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a): pass
            def do_GET(self):
                try:
                    if self.path in ("/", "/index.html"):
                        self.send_response(200)
                        self.send_header("Content-Type", "text/html; charset=utf-8")
                        self.send_header("Content-Length", str(len(html_bytes)))
                        self.end_headers(); self.wfile.write(html_bytes)
                    elif self.path == "/connected":
                        parent.root.after(0, parent._close_qr_window)
                        self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
                    elif self.path.startswith("/ask?"):
                        qs = urllib.parse.parse_qs(self.path.split("?",1)[1])
                        question = qs.get("q", [""])[0]
                        answer = parent.ask_anything(question, speak_answer=False)
                        data = json.dumps({"answer": answer}, ensure_ascii=False).encode("utf-8")
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json; charset=utf-8")
                        self.send_header("Content-Length", str(len(data)))
                        self.end_headers(); self.wfile.write(data)
                    elif self.path == "/nowplaying":
                        i = parent.get_now_playing()
                        if i and i.get("title"):
                            p = {"playing": True, "title": i.get("title",""), "artist": i.get("artist",""),
                                 "album": i.get("album",""), "has_cover": bool(i.get("cover_bytes"))}
                        else:
                            p = {"playing": False, "title":"", "artist":"", "album":"", "has_cover": False}
                        d = json.dumps(p, ensure_ascii=False).encode("utf-8")
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json; charset=utf-8")
                        self.send_header("Content-Length", str(len(d)))
                        self.send_header("Cache-Control", "no-store")
                        self.end_headers(); self.wfile.write(d)
                    elif self.path == "/stats":
                        d = json.dumps({"cpu": psutil.cpu_percent(interval=0),
                                        "ram": psutil.virtual_memory().percent}).encode()
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Content-Length", str(len(d)))
                        self.send_header("Cache-Control", "no-store")
                        self.end_headers(); self.wfile.write(d)
                    elif self.path.startswith("/cover"):
                        c = parent.get_cover_bytes()
                        if c:
                            self.send_response(200)
                            self.send_header("Content-Type", "image/jpeg")
                            self.send_header("Content-Length", str(len(c)))
                            self.send_header("Cache-Control", "no-cache")
                            self.end_headers(); self.wfile.write(c)
                        else:
                            self.send_response(204); self.end_headers()
                    elif self.path.startswith("/cmd/"):
                        cmd = self.path[5:].split("?")[0]
                        parent._handle_remote_command(cmd)
                        self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
                    else:
                        self.send_response(404); self.end_headers()
                except (BrokenPipeError, ConnectionResetError): pass

        try:
            socketserver.TCPServer.allow_reuse_address = True
            self.control_server = socketserver.TCPServer(("0.0.0.0", CONTROL_PORT), H)
            self.control_server_thread = threading.Thread(target=self.control_server.serve_forever, daemon=True)
            self.control_server_thread.start()
            self.control_server_running = True
            self.show_notification("Telefon Kontrol", f"Aktif: {CONTROL_PORT}", duration=3000)
            self.root.after(200, self.show_qr_code)
        except Exception as e:
            messagebox.showerror("Sunucu", f"{e}")

    def stop_control_server(self):
        if self.control_server and self.control_server_running:
            try: self.control_server.shutdown(); self.control_server.server_close()
            except Exception: pass
            self.control_server_running = False

    def show_qr_code(self):
        if not self.control_server_running: self.start_control_server(); return
        if not QR_AVAILABLE:
            messagebox.showinfo("QR", f"http://{self._get_local_ip()}:{CONTROL_PORT}"); return
        if self.qr_window and self.qr_window.winfo_exists(): self.qr_window.lift(); return
        ip = self._get_local_ip(); url = f"http://{ip}:{CONTROL_PORT}"
        qr = qrcode.QRCode(version=1, box_size=8, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(url); qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        img = img.resize((260, 260), Image.NEAREST); photo = ImageTk.PhotoImage(img)
        self.qr_window = Toplevel(self.root)
        self.qr_window.title("Telefondan Kontrol")
        self.qr_window.configure(bg=self.bg); self.qr_window.attributes('-topmost', True)
        self.qr_window.geometry(f"320x400+{self.root.winfo_x()}+{self.root.winfo_y()-420}")
        Label(self.qr_window, text="📱 Telefondan Kontrol", fg=self.style["fg_main"], bg=self.bg,
              font=("Segoe UI", 13, "bold")).pack(pady=(12, 4))
        Label(self.qr_window, text="Kamera ile QR kodu okut", fg=self.style["fg_text"], bg=self.bg,
              font=("Segoe UI", 9)).pack(pady=(0, 8))
        l = Label(self.qr_window, image=photo, bg="white", bd=0); l.image = photo; l.pack(pady=4)
        Label(self.qr_window, text=url, fg=self.style["fg_secondary"], bg=self.bg,
              font=("Consolas", 9)).pack(pady=(8, 4))
        bf = tk.Frame(self.qr_window, bg=self.bg); bf.pack(pady=(4, 12))
        tk.Button(bf, text="🔗 Aç", command=lambda: webbrowser.open(url),
                  bg=self.style["button_bg"], fg=self.style["fg_text"], bd=0, padx=12, pady=5,
                  cursor="hand2").pack(side=tk.LEFT, padx=4)
        tk.Button(bf, text="Kapat", command=lambda: (self.stop_control_server(), self.qr_window.destroy()),
                  bg="#FF5252", fg="white", bd=0, padx=12, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=4)

    def _close_qr_window(self):
        try:
            if self.qr_window and self.qr_window.winfo_exists():
                self.qr_window.destroy(); self.qr_window = None
                self.show_notification("Telefon Kontrol", "📱 Bağlandı ✓", duration=2000)
        except Exception: pass

    # ============================================================
    # GÜNCELLEME & WEB SUNUCU
    # ============================================================
    def check_for_updates_background(self):
        while True:
            if self.online: self.check_for_updates()
            time.sleep(3600)

    def check_for_updates(self):
        try:
            req = urllib.request.Request(GITHUB_REPO_API, headers={'User-Agent': 'NexusBar'})
            with urllib.request.urlopen(req, timeout=5) as r:
                d = json.loads(r.read().decode())
                if d.get("tag_name","0.0") > CURRENT_VERSION:
                    self.show_notification("Güncelleme", f"Yeni: {d.get('tag_name')}", duration=8000)
        except Exception: pass

    def toggle_web_server(self):
        if self.web_server_running: self.stop_web_server()
        else: self.start_web_server()

    def start_web_server(self):
        if self.web_server_running: return
        desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
        PORT = 8080
        class QH(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *a, **kw): super().__init__(*a, directory=desktop, **kw)
            def log_message(self, *a): pass
        try:
            self.web_server = socketserver.TCPServer(("", PORT), QH)
            self.web_server_thread = threading.Thread(target=self.web_server.serve_forever, daemon=True)
            self.web_server_thread.start(); self.web_server_running = True
            self.show_notification("Web", f"http://{self._get_local_ip()}:{PORT}", duration=5000)
        except Exception as e: messagebox.showerror("Web", f"{e}")

    def stop_web_server(self):
        if self.web_server and self.web_server_running:
            self.web_server.shutdown(); self.web_server.server_close(); self.web_server_running = False

    # ============================================================
    # AYARLAR
    # ============================================================
    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f: return json.load(f)
            except Exception: pass
        return {}

    def save_settings(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump({"clock_24h": self.clock_24h, "show_date": self.show_date,
                           "theme": self.current_theme, "username": self.current_user,
                           "profile_image_path": self.profile_image_path,
                           "assistant_enabled": self.assistant_enabled,
                           "groq_api_key": self.settings.get("groq_api_key", GROQ_API_KEY)},
                          f, ensure_ascii=False, indent=4)
        except Exception: pass

    def set_clock_format(self, i, s):
        self.clock_24h = i; self.show_date = s; self.date_var.set(s); self.save_settings()

    def toggle_date(self):
        self.show_date = self.date_var.get(); self.save_settings()

    # ============================================================
    # ARAYÜZ
    # ============================================================
    def _create_widgets(self):
        if self.user_image:
            self.profile_btn = tk.Button(self.main_frame, image=self.user_image, command=self.show_profile_popup,
                                         bg=self.bg, bd=0, cursor="hand2", activebackground=self.bg)
        else:
            self.profile_btn = tk.Button(self.main_frame, text="👤", command=self.show_profile_popup,
                                         bg=self.bg, fg=self.style["fg_text"], bd=0,
                                         font=("Segoe UI", 12), cursor="hand2", activebackground=self.bg)
        self.profile_btn.pack(side=tk.LEFT, padx=(0, 6), pady=2)

        self.status_canvas = tk.Canvas(self.main_frame, width=40, height=40, bg=self.bg, highlightthickness=0)
        self.status_canvas.pack(side=tk.LEFT, padx=4)
        self.outer_circle = self.status_canvas.create_oval(2, 2, 38, 38, outline="#FF5252", width=3)
        self.cloud1 = self.status_canvas.create_oval(10, 15, 22, 22, fill="#FFFFFF", outline="")
        self.cloud2 = self.status_canvas.create_oval(18, 18, 30, 25, fill="#FFFFFF", outline="")
        self.cloud3 = self.status_canvas.create_oval(14, 12, 26, 18, fill="#FFFFFF", outline="")
        self.status_dot = self.status_canvas.create_oval(17, 17, 23, 23, fill="#FF5252", outline="")
        self.status_canvas.bind("<Button-1>", lambda e: self.toggle_assistant())

        cf = tk.Frame(self.main_frame, bg=self.bg); cf.pack(side=tk.LEFT, padx=6)
        self.cpu_label = Label(cf, text="CPU", fg=self.style["fg_main"], bg=self.bg, font=self.font_label)
        self.cpu_label.pack(anchor=tk.CENTER)
        self.cpu_canvas = tk.Canvas(cf, width=60, height=8, bg=self.style["bar_bg"], highlightthickness=0)
        self.cpu_canvas.pack(pady=2)
        self.cpu_bar = self.cpu_canvas.create_rectangle(0, 0, 0, 8, fill=self.style["fg_main"], outline="")
        self.cpu_val = Label(cf, text="0%", fg=self.style["fg_text"], bg=self.bg, font=self.font_value)
        self.cpu_val.pack(anchor=tk.CENTER)

        rf = tk.Frame(self.main_frame, bg=self.bg); rf.pack(side=tk.LEFT, padx=6)
        self.ram_label = Label(rf, text="RAM", fg=self.style["fg_secondary"], bg=self.bg, font=self.font_label)
        self.ram_label.pack(anchor=tk.CENTER)
        self.ram_canvas = tk.Canvas(rf, width=60, height=8, bg=self.style["bar_bg"], highlightthickness=0)
        self.ram_canvas.pack(pady=2)
        self.ram_bar = self.ram_canvas.create_rectangle(0, 0, 0, 8, fill=self.style["fg_secondary"], outline="")
        self.ram_val = Label(rf, text="0%", fg=self.style["fg_text"], bg=self.bg, font=self.font_value)
        self.ram_val.pack(anchor=tk.CENTER)

        df = tk.Frame(self.main_frame, bg=self.bg); df.pack(side=tk.LEFT, padx=6)
        self.disk_label = Label(df, text="DISK", fg=self.style["fg_warning"], bg=self.bg, font=self.font_label)
        self.disk_label.pack(anchor=tk.CENTER)
        self.disk_canvas = tk.Canvas(df, width=60, height=8, bg=self.style["bar_bg"], highlightthickness=0)
        self.disk_canvas.pack(pady=2)
        self.disk_bar = self.disk_canvas.create_rectangle(0, 0, 0, 8, fill=self.style["fg_warning"], outline="")
        self.disk_val = Label(df, text="0%", fg=self.style["fg_text"], bg=self.bg, font=self.font_value)
        self.disk_val.pack(anchor=tk.CENTER)

        nf = tk.Frame(self.main_frame, bg=self.bg); nf.pack(side=tk.LEFT, padx=6)
        Label(nf, text="🌐", fg=self.style["fg_secondary"], bg=self.bg, font=self.font_label).pack(anchor=tk.CENTER)
        self.net_down_label = Label(nf, text="↓0K", fg=self.style["fg_main"], bg=self.bg, font=self.font_value)
        self.net_down_label.pack(anchor=tk.CENTER)
        self.net_up_label = Label(nf, text="↑0K", fg=self.style["fg_warning"], bg=self.bg, font=self.font_small)
        self.net_up_label.pack(anchor=tk.CENTER)

        bf = tk.Frame(self.main_frame, bg=self.bg); bf.pack(side=tk.LEFT, padx=6)
        self.brightness_label = Label(bf, text="☀️", fg=self.style["fg_warning"], bg=self.bg, font=self.font_label)
        self.brightness_label.pack(anchor=tk.CENTER)
        self.brightness_val = Label(bf, text="---", fg=self.style["fg_text"], bg=self.bg, font=self.font_value)
        self.brightness_val.pack(anchor=tk.CENTER)
        for w in (bf, self.brightness_label, self.brightness_val): w.bind("<MouseWheel>", self.adjust_brightness)

        uf = tk.Frame(self.main_frame, bg=self.bg); uf.pack(side=tk.LEFT, padx=6)
        Label(uf, text="⏳", fg=self.style["fg_text"], bg=self.bg, font=self.font_small).pack(anchor=tk.CENTER)
        self.uptime_val = Label(uf, text="00:00", fg=self.style["fg_text"], bg=self.bg, font=self.font_value)
        self.uptime_val.pack(anchor=tk.CENTER)

        inf = tk.Frame(self.main_frame, bg=self.bg); inf.pack(side=tk.LEFT, padx=6)
        self.inet_dot = tk.Canvas(inf, width=10, height=10, bg=self.bg, highlightthickness=0)
        self.inet_dot.pack(pady=1); self.inet_dot.create_oval(1, 1, 9, 9, fill="#FF5252", outline="")
        self.inet_text = Label(inf, text="OFF", fg="#FF5252", bg=self.bg, font=self.font_small)
        self.inet_text.pack(anchor=tk.CENTER)

        wf = tk.Frame(self.main_frame, bg=self.bg); wf.pack(side=tk.LEFT, padx=6)
        self.weather_icon_label = Label(wf, text="🌤", fg=self.style["fg_secondary"], bg=self.bg,
                                         font=self.font_weather, cursor="hand2")
        self.weather_icon_label.pack(anchor=tk.CENTER)
        self.weather_icon_label.bind("<Button-1>", self.show_weather_detail)
        self.weather_temp_label = Label(wf, text="---°C", fg=self.style["fg_text"], bg=self.bg, font=self.font_value)
        self.weather_temp_label.pack(anchor=tk.CENTER)

        self.clean_btn = tk.Button(self.main_frame, text="🧹", command=self.clean_temp_and_recycle,
                                   bg=self.style["button_bg"], fg=self.style["fg_text"], bd=0, font=("Segoe UI", 10),
                                   activebackground="#3A3A5C", activeforeground="#FFD54F", cursor="hand2")
        self.clean_btn.pack(side=tk.LEFT, padx=6)

        self.mic_btn = tk.Button(self.main_frame, text="🎤" if self.assistant_enabled else "🔇",
                                 command=self.toggle_assistant, bg=self.style["button_bg"], fg=self.style["fg_text"],
                                 bd=0, font=("Segoe UI", 10), activebackground="#3A3A5C",
                                 activeforeground="#FFD54F", cursor="hand2")
        self.mic_btn.pack(side=tk.LEFT, padx=4)

        self.privacy_btn = tk.Button(self.main_frame, text="🕶️", command=self.toggle_privacy,
                                     bg=self.style["button_bg"], fg=self.style["fg_text"], bd=0,
                                     font=("Segoe UI", 10), activebackground="#3A3A5C",
                                     activeforeground="#FFD54F", cursor="hand2")
        self.privacy_btn.pack(side=tk.LEFT, padx=4)

        self.clock_text = Label(self.main_frame, text="00:00", fg=self.style["fg_clock"], bg=self.bg,
                                font=("Segoe UI", 12, "bold"))
        self.clock_text.pack(side=tk.LEFT, padx=6)
        self.clock_text.bind("<Double-Button-1>", self.toggle_big_clock)

    # ============================================================
    # BÜYÜK SAAT
    # ============================================================
    def toggle_big_clock(self, event=None):
        if self.big_clock: self.big_clock.destroy(); self.big_clock = None
        else:
            self.big_clock = Toplevel(self.root); self.big_clock.overrideredirect(True)
            self.big_clock.attributes('-topmost', True); self.big_clock.attributes('-alpha', 0.85)
            self.big_clock.configure(bg=self.style["bg"])
            self.big_clock_label = Label(self.big_clock, text=self._format_clock_text(),
                                          fg=self.style["fg_clock"], bg=self.style["bg"],
                                          font=("Segoe UI", 72, "bold"))
            self.big_clock_label.pack(padx=40, pady=20)
            self.big_clock.geometry(f"+{self.root.winfo_x()+200}+{self.root.winfo_y()-200}")
            self.big_clock.bind("<Button-1>", lambda e: (setattr(self, 'bx', e.x), setattr(self, 'by', e.y)))
            self.big_clock.bind("<B1-Motion>", self.on_motion_big)
            self.big_clock.bind("<Double-Button-1>", lambda e: self.toggle_big_clock())
            self.update_big_clock()

    def update_big_clock(self):
        if self.big_clock:
            self.big_clock_label.config(text=self._format_clock_text())
            self.root.after(200, self.update_big_clock)

    def on_motion_big(self, event):
        x = self.big_clock.winfo_x() + (event.x - getattr(self, 'bx', 0))
        y = self.big_clock.winfo_y() + (event.y - getattr(self, 'by', 0))
        self.big_clock.geometry(f"+{x}+{y}")

    # ============================================================
    # EKRAN / GİZLİLİK / GÖREV
    # ============================================================
    def take_screenshot(self):
        try:
            desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
            fn = f"ekran_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            ImageGrab.grab().save(os.path.join(desktop, fn), "PNG")
            self.show_notification("Ekran", fn, duration=2000)
        except Exception as e: messagebox.showerror("Hata", f"{e}")

    def toggle_privacy(self):
        for k in (0x5B, 0x44): ctypes.windll.user32.keybd_event(k, 0, 0, 0)
        for k in (0x44, 0x5B): ctypes.windll.user32.keybd_event(k, 0, 2, 0)

    def show_task_manager(self):
        AnimatedTaskManager(self.root, self.style["bg"], self.style["fg_text"],
                            self.style["button_bg"], self.root.winfo_y(), self.root.winfo_height())

    # ============================================================
    # SAĞ TIK MENÜSÜ
    # ============================================================
    def build_context_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0, bg="#2A2A40", fg="#E0E0E0",
                            activebackground=self.style["fg_main"], activeforeground="#000")
        tm = tk.Menu(self.menu, tearoff=0, bg="#2A2A40", fg="#E0E0E0")
        for name, lbl in [("Koyu","🌙 Koyu"),("Açık","☀️ Açık"),("Neon","💜 Neon"),("Şeffaf","👻 Şeffaf")]:
            tm.add_command(label=lbl, command=lambda n=name: self.change_theme(n))
        om = tk.Menu(self.menu, tearoff=0, bg="#2A2A40", fg="#E0E0E0")
        for p in (0.3, 0.5, 0.7, 0.9, 1.0):
            om.add_command(label=f"%{int(p*100)}", command=lambda v=p: self.set_opacity(v))
        cm = tk.Menu(self.menu, tearoff=0, bg="#2A2A40", fg="#E0E0E0")
        cm.add_command(label="24 Saat", command=lambda: self.set_clock_format(True, self.show_date))
        cm.add_command(label="12 Saat", command=lambda: self.set_clock_format(False, self.show_date))
        cm.add_separator()
        self.date_var = tk.BooleanVar(value=self.show_date)
        cm.add_checkbutton(label="Tarihi Göster", variable=self.date_var, command=self.toggle_date)

        self.menu.add_command(label=f"🎤 {ASSISTANT_NAME} Aç/Kapat", command=self.toggle_assistant)
        self.menu.add_command(label="📱 Telefondan Kontrol (QR)", command=self.show_qr_code)
        self.menu.add_command(label="🧠 Groq AI Test Et", command=self.test_groq)
        self.menu.add_command(label="🔑 Groq API Anahtarı Gir", command=self.set_groq_key_dialog)
        self.menu.add_command(label="👤 Profil", command=self.show_profile_popup)
        self.menu.add_command(label="📷 Profil Fotoğrafı Seç", command=self.choose_profile_image)
        self.menu.add_command(label="🔄 Güncellemeyi Kontrol Et", command=self.check_for_updates)
        self.menu.add_command(label="🌐 Web Sunucusu", command=self.toggle_web_server)
        self.menu.add_separator()
        self.menu.add_command(label="🍅 Pomodoro Başlat (25dk)", command=lambda: self.start_pomodoro(25))
        water_label = "💧 Su Hatırlatıcı Kapat" if self.water_reminder_active else "💧 Su Hatırlatıcı Aç"
        self.menu.add_command(label=water_label, command=self.toggle_water_reminder)
        auto_label = "🚀 Otomatik Başlatmayı Kapat" if self.is_autostart_enabled() else "🚀 Otomatik Başlatmayı Aç"
        self.menu.add_command(label=auto_label, command=self.toggle_autostart)
        self.menu.add_separator()
        self.menu.add_command(label="🎵 Müzik Aç", command=self.open_music_app)
        self.menu.add_command(label="🔕 Müzik Kapat", command=self.close_music_app)
        self.menu.add_separator()
        self.menu.add_command(label="🧹 Temizle", command=self.clean_temp_and_recycle)
        self.menu.add_command(label="📋 Görev Yöneticisi", command=self.show_task_manager)
        self.menu.add_command(label="📷 Ekran Görüntüsü Al", command=self.take_screenshot)
        self.menu.add_separator()
        self.menu.add_cascade(label="🎨 Tema", menu=tm)
        self.menu.add_cascade(label="🔍 Saydamlık", menu=om)
        self.menu.add_cascade(label="🕒 Saat Formatı", menu=cm)
        self.menu.add_separator()
        self.always_top_var = tk.BooleanVar(value=True)
        self.menu.add_checkbutton(label="📌 Her Zaman Üstte", variable=self.always_top_var, command=self.toggle_always_on_top)
        self.menu.add_command(label="🔒 Pencereyi Kilitle", command=self.toggle_lock_window)
        self.menu.add_separator()
        self.menu.add_command(label="ℹ️ Hakkında", command=self.show_about)
        self.menu.add_separator()
        self.menu.add_command(label="⬇️ Sistem Tepsisine Küçült", command=self.minimize_to_tray)
        self.menu.add_command(label="❌ Çıkış", command=self.quit_app)

        try:
            for i in range(self.menu.index("end") + 1):
                try: lbl = self.menu.entrycget(i, "label") if self.menu.type(i) != "separator" else ""
                except Exception: lbl = ""
                if lbl and "Pencereyi Kilitle" in lbl:
                    self.lock_menu_index = i; break
        except Exception: self.lock_menu_index = 0

    def show_menu(self, event):
        try:
            if self.window_locked: self.menu.entryconfigure(self.lock_menu_index, label="🔓 Kilidi Aç")
            else: self.menu.entryconfigure(self.lock_menu_index, label="🔒 Pencereyi Kilitle")
        except Exception: pass
        self.menu.tk_popup(event.x_root, event.y_root)

    def _format_clock_text(self):
        n = datetime.datetime.now()
        t = n.strftime("%H:%M") if self.clock_24h else n.strftime("%I:%M %p")
        return f"{n.strftime('%d.%m.%Y')}\n{t}" if self.show_date else t

    # ============================================================
    # İŞLEV METODLARI
    # ============================================================
    def toggle_assistant(self):
        if self.assistant_running: self.stop_assistant()
        else: self.start_assistant()

    def set_opacity(self, a): self.root.attributes('-alpha', a); self.style["alpha"] = a

    def toggle_always_on_top(self):
        self.always_on_top = self.always_top_var.get()
        self.root.attributes('-topmost', self.always_on_top)

    def toggle_lock_window(self):
        self.window_locked = not self.window_locked
        if self.window_locked:
            for ev in ("<Button-1>", "<ButtonRelease-1>", "<B1-Motion>"): self.main_frame.unbind(ev)
        else:
            self.main_frame.bind("<Button-1>", self.start_move)
            self.main_frame.bind("<ButtonRelease-1>", self.stop_move)
            self.main_frame.bind("<B1-Motion>", self.on_motion)

    def change_theme(self, name):
        self.current_theme = name; self.style = self.themes[name]; self.bg = self.style["bg"]
        a = self.style.get("alpha", 0.9)
        self.root.configure(bg=self.bg); self.root.attributes('-alpha', a); self.main_frame.configure(bg=self.bg)
        self.profile_btn.configure(bg=self.bg, activebackground=self.bg)
        if not self.user_image: self.profile_btn.configure(fg=self.style["fg_text"])
        self.status_canvas.configure(bg=self.bg); self.update_status_dot()
        for w in self.main_frame.winfo_children():
            if isinstance(w, tk.Frame):
                w.configure(bg=self.bg)
                for c in w.winfo_children():
                    try:
                        if isinstance(c, (Label, tk.Button)) and c not in [self.clean_btn, self.mic_btn, self.privacy_btn, self.profile_btn]:
                            c.configure(bg=self.bg)
                    except Exception: pass
        self.cpu_label.configure(fg=self.style["fg_main"], bg=self.bg)
        self.cpu_canvas.configure(bg=self.style["bar_bg"]); self.cpu_val.configure(fg=self.style["fg_text"], bg=self.bg)
        self.ram_label.configure(fg=self.style["fg_secondary"], bg=self.bg)
        self.ram_canvas.configure(bg=self.style["bar_bg"]); self.ram_val.configure(fg=self.style["fg_text"], bg=self.bg)
        self.disk_label.configure(fg=self.style["fg_warning"], bg=self.bg)
        self.disk_canvas.configure(bg=self.style["bar_bg"]); self.disk_val.configure(fg=self.style["fg_text"], bg=self.bg)
        self.net_down_label.configure(fg=self.style["fg_main"], bg=self.bg)
        self.net_up_label.configure(fg=self.style["fg_warning"], bg=self.bg)
        self.brightness_label.configure(fg=self.style["fg_warning"], bg=self.bg)
        self.brightness_val.configure(fg=self.style["fg_text"], bg=self.bg)
        self.uptime_val.configure(fg=self.style["fg_text"], bg=self.bg)
        self.inet_dot.configure(bg=self.bg); self.inet_text.configure(bg=self.bg)
        self.weather_icon_label.configure(fg=self.style["fg_secondary"], bg=self.bg)
        self.weather_temp_label.configure(fg=self.style["fg_text"], bg=self.bg)
        self.clean_btn.configure(bg=self.style["button_bg"], fg=self.style["fg_text"])
        self.mic_btn.configure(bg=self.style["button_bg"], fg=self.style["fg_text"])
        self.privacy_btn.configure(bg=self.style["button_bg"], fg=self.style["fg_text"])
        self.clock_text.configure(fg=self.style["fg_clock"], bg=self.bg)
        self.build_context_menu(); self.save_settings()

    def show_about(self):
        a = Toplevel(self.root); a.title("Nexus Bar"); a.geometry("380x340"); a.resizable(False, False)
        a.configure(bg=self.bg); a.attributes('-topmost', True)
        f = tk.Frame(a, bg=self.bg, padx=20, pady=20); f.pack(expand=True, fill=tk.BOTH)
        Label(f, text="🦁 Nexus Bar", fg=self.style["fg_clock"], bg=self.bg, font=("Segoe UI", 16, "bold")).pack(pady=(0,10))
        Label(f, text=f"Sürüm {CURRENT_VERSION}", fg=self.style["fg_text"], bg=self.bg, font=("Segoe UI", 10)).pack()
        Label(f, text="🎤 Sesli Asistan + 🧠 Yapay Zeka", fg=self.style["fg_secondary"], bg=self.bg, font=("Segoe UI", 9)).pack(pady=(5,0))
        Label(f, text="Wikipedia · DuckDuckGo · Groq (Llama 3.1/3.3/4)", fg=self.style["fg_warning"], bg=self.bg, font=("Segoe UI", 9, "italic")).pack(pady=(6,0))
        Label(f, text='"Einstein kimdir?" diye sor', fg=self.style["fg_secondary"], bg=self.bg, font=("Segoe UI", 8)).pack()
        Label(f, text="Python ile yapıldı ❤️", fg=self.style["fg_warning"], bg=self.bg, font=("Segoe UI", 8)).pack(pady=(10,0))
        tk.Button(f, text="Tamam", command=a.destroy, bg=self.style["button_bg"],
                  fg=self.style["fg_text"], bd=0, padx=20, pady=5).pack(pady=(10,0))

    # ============================================================
    # HAVA
    # ============================================================
    def fetch_location_and_weather(self):
        try:
            r = urllib.request.Request("http://ip-api.com/json/", headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(r, timeout=5) as res:
                d = json.loads(res.read().decode())
                self.city = d.get("city", "Istanbul")
                self.lat = d.get("lat", 41.0082); self.lon = d.get("lon", 28.9784)
        except Exception: pass
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto&forecast_days=5"
            r = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(r, timeout=5) as res:
                w = json.loads(res.read().decode()); dd = w.get("daily", {})
                dates, mx, mn, cd = dd.get("time", []), dd.get("temperature_2m_max", []), dd.get("temperature_2m_min", []), dd.get("weathercode", [])
                fc = [{"date": dates[i], "max_temp": mx[i] if i < len(mx) else "--",
                       "min_temp": mn[i] if i < len(mn) else "--",
                       "icon": self.get_weather_icon(int(cd[i]) if i < len(cd) else 0),
                       "description": self.get_weather_description(int(cd[i]) if i < len(cd) else 0)} for i in range(len(dates))]
                if fc:
                    self.weather_cache = {"current": fc[0], "daily": fc}
                    self.weather_icon_label.config(text=fc[0]["icon"])
                    self.weather_temp_label.config(text=f"{fc[0]['min_temp']}° / {fc[0]['max_temp']}°")
        except Exception:
            self.weather_cache = {}; self.weather_icon_label.config(text="❓")

    def get_weather_icon(self, c):
        if c in (0,1): return "☀️"
        if c == 2: return "🌤"
        if c == 3: return "☁️"
        if c in (45,48): return "🌫"
        if c in (51,53,55,61,63,65): return "🌧"
        if c in (71,73,75): return "🌨"
        if c in (80,81,82): return "🌦"
        if c in (95,96,99): return "⛈"
        return "🌤"

    def get_weather_description(self, c):
        return {0:"Açık",1:"Az bulutlu",2:"Parçalı bulutlu",3:"Bulutlu",45:"Sisli",48:"Kırağı",
                51:"Hafif çisenti",53:"Çisenti",55:"Yoğun çisenti",61:"Hafif yağmur",63:"Yağmur",
                65:"Şiddetli yağmur",71:"Hafif kar",73:"Kar",75:"Yoğun kar",80:"Hafif sağanak",
                81:"Sağanak",82:"Şiddetli sağanak",95:"Gök gürültülü",96:"Dolu",99:"Şiddetli dolu"}.get(c, "")

    def weather_scheduler(self):
        while True: time.sleep(600); self.fetch_location_and_weather()

    def show_weather_detail(self, event=None):
        if "daily" not in self.weather_cache or not self.weather_cache["daily"]:
            messagebox.showinfo("Hava", "Yüklenmedi."); return
        AnimatedWeatherPanel(self.root, self.weather_cache["daily"], self.city,
                              self.style, self.root.winfo_y(), self.root.winfo_height())

    # ============================================================
    # DİĞER
    # ============================================================
    def register_hotkey(self):
        try: user32.RegisterHotKey(self.root.winfo_id(), HOTKEY_ID, MOD_CTRL_SHIFT, VK_N)
        except Exception: pass

    def create_tray_icon(self):
        img = Image.new("RGBA", (64, 64), (0,0,0,0)); d = ImageDraw.Draw(img)
        d.ellipse([8,8,56,56], fill="#FF8C00", outline="#FFD54F", width=2)
        d.ellipse([20,22,28,30], fill="#1C1C2E"); d.ellipse([36,22,44,30], fill="#1C1C2E")
        d.polygon([(30,34),(34,34),(32,38)], fill="#1C1C2E")
        d.arc([24,36,40,48], start=0, end=180, fill="#1C1C2E", width=2)
        self.tray_icon = pystray.Icon("nexus_bar", img, "Nexus Bar", menu=pystray.Menu(
            pystray.MenuItem("Göster", self.show_window),
            pystray.MenuItem("QR Kontrol", self.show_qr_code),
            pystray.MenuItem("Groq Test", self.test_groq),
            pystray.MenuItem("Pomodoro", lambda: self.start_pomodoro(25)),
            pystray.MenuItem("Su Hatırlatıcı", self.toggle_water_reminder),
            pystray.MenuItem("Müzik Aç", self.open_music_app),
            pystray.MenuItem("Müzik Kapat", self.close_music_app),
            pystray.MenuItem("Çıkış", self.quit_app)))
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def minimize_to_tray(self): self.root.withdraw()

    def show_window(self):
        self.root.deiconify(); self.root.lift()
        self.root.attributes('-topmost', self.always_on_top)

    def quit_app(self):
        self.stop_assistant()
        if self.web_server_running: self.stop_web_server()
        if self.control_server_running: self.stop_control_server()
        if self.tray_icon: self.tray_icon.stop()
        try: user32.UnregisterHotKey(self.root.winfo_id(), HOTKEY_ID)
        except Exception: pass
        self.root.destroy()

    def start_move(self, event):
        if not self.window_locked: self.x, self.y = event.x, event.y

    def stop_move(self, event):
        if not self.window_locked:
            self.x, self.y = None, None; self.snap_to_edge()

    def on_motion(self, event):
        if not self.window_locked:
            self.root.geometry(f"+{self.root.winfo_x()+event.x-self.x}+{self.root.winfo_y()+event.y-self.y}")

    def snap_to_edge(self):
        if self.window_locked: return
        x, y = self.root.winfo_x(), self.root.winfo_y()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        nx, ny = x, y
        if x < self.snap_margin: nx = 0
        elif (x + w) > (sw - self.snap_margin): nx = sw - w
        if y < self.snap_margin: ny = 0
        elif (y + h) > (sh - self.snap_margin): ny = sh - h
        if nx != x or ny != y:
            self.root.geometry(f"+{nx}+{ny}")
            n = time.time()
            if n - self.last_collision_time > self.collision_cooldown:
                self.last_collision_time = n; self.flash_effect()

    def flash_effect(self):
        fc = self.style.get("flash", "#FFFFFF")
        ws = [self.main_frame] + list(self.main_frame.winfo_children())
        for w in ws:
            if isinstance(w, (tk.Frame, tk.Canvas)):
                try: w.configure(bg=fc)
                except Exception: pass
        self.root.after(80, lambda: self.restore_flash(ws))
        try: winsound.Beep(800, 50)
        except Exception: pass

    def restore_flash(self, ws):
        for w in ws:
            if isinstance(w, (tk.Frame, tk.Canvas)):
                try: w.configure(bg=self.bg)
                except Exception: pass

    def show_notification(self, title, message, duration=4000):
        n = Toplevel(self.root); n.overrideredirect(True); n.attributes('-topmost', True)
        n.configure(bg="#2A2A40")
        n.geometry(f"320x80+{self.root.winfo_x()+200}+{self.root.winfo_y()-90}")
        Label(n, text=title, fg="#FF5252", bg="#2A2A40", font=("Segoe UI", 10, "bold")).pack(pady=(8,0))
        Label(n, text=message, fg="#E0E0E0", bg="#2A2A40", font=("Segoe UI", 9), wraplength=300).pack()
        n.after(duration, n.destroy)

    def clean_temp_and_recycle(self):
        self.clean_btn.config(text="⌛", state="disabled")
        cnt = 0
        try:
            for root, _, files in os.walk(tempfile.gettempdir()):
                for f in files:
                    try: os.unlink(os.path.join(root, f)); cnt += 1
                    except Exception: pass
        except Exception: pass
        rc = False
        try: ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0); rc = True
        except Exception: pass
        messagebox.showinfo("Temizlik", f"Geçici: {cnt} dosya\n" + ("Çöp boşaltıldı." if rc else "Çöp temizlenemedi."))
        self.clean_btn.config(text="🧹", state="normal")

    def internet_checker(self):
        endpoints = ["https://api.groq.com/", "https://duckduckgo.com/",
                     "https://www.google.com/generate_204", "https://1.1.1.1/"]
        while True:
            ok = False
            for url in endpoints:
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "NexusBar/1.0"})
                    with urllib.request.urlopen(req, timeout=6) as r:
                        ok = True; break
                except Exception: continue
            prev = self.online
            self.online = ok
            if prev != self.online:
                m = "Bağlantı geldi ✓" if self.online else "Bağlantı kesildi!"
                self.root.after(0, lambda msg=m: self.show_notification("İnternet", msg))
            time.sleep(15)

    def get_brightness(self):
        try:
            h = ctypes.windll.user32.MonitorFromPoint(0, MONITOR_DEFAULT_TO_PRIMARY)
            mn, cur, mx = wintypes.DWORD(), wintypes.DWORD(), wintypes.DWORD()
            if ctypes.windll.dxva2.GetMonitorBrightness(h, ctypes.byref(mn), ctypes.byref(cur), ctypes.byref(mx)):
                return int(cur.value / mx.value * 100)
        except Exception: pass
        return -1

    def set_brightness(self, v):
        try:
            h = ctypes.windll.user32.MonitorFromPoint(0, MONITOR_DEFAULT_TO_PRIMARY)
            ctypes.windll.dxva2.SetMonitorBrightness(h, int(v)); return True
        except Exception: return False

    def update_brightness_display(self):
        b = self.get_brightness()
        self.brightness_val.config(text=f"{b}%" if b >= 0 else "N/A")

    def adjust_brightness(self, e):
        c = self.get_brightness()
        if c < 0: return
        n = min(100, c + 10) if e.delta > 0 else max(0, c - 10)
        self.set_brightness(n); self.update_brightness_display()

    def get_uptime(self):
        s = time.time() - psutil.boot_time()
        return f"{int(s//3600):02d}:{int((s%3600)//60):02d}"

    def update_system_info(self):
        cpu = psutil.cpu_percent(interval=0.0)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('C:\\').percent
        self.cpu_canvas.coords(self.cpu_bar, 0, 0, int(cpu * 0.6), 8); self.cpu_val.config(text=f"{cpu:.0f}%")
        self.ram_canvas.coords(self.ram_bar, 0, 0, int(mem * 0.6), 8); self.ram_val.config(text=f"{mem:.0f}%")
        self.disk_canvas.coords(self.disk_bar, 0, 0, int(disk * 0.6), 8); self.disk_val.config(text=f"{disk:.0f}%")
        self.uptime_val.config(text=self.get_uptime())
        nt = time.time(); el = nt - self.last_net_time
        if el >= 0.9:
            try:
                n = psutil.net_io_counters()
                dk = (n.bytes_recv - self.last_net_io.bytes_recv) / el / 1024
                uk = (n.bytes_sent - self.last_net_io.bytes_sent) / el / 1024
                self.last_net_io = n; self.last_net_time = nt
                def fmt(kb): return f"{kb/1024:.1f}M" if kb >= 1024 else f"{kb:.0f}K"
                self.net_down_label.config(text=f"↓{fmt(dk)}")
                self.net_up_label.config(text=f"↑{fmt(uk)}")
            except Exception: pass
        if self.online:
            self.inet_dot.itemconfig(1, fill="#69F0AE"); self.inet_text.config(text="ON", fg="#69F0AE")
        else:
            self.inet_dot.itemconfig(1, fill="#FF5252"); self.inet_text.config(text="OFF", fg="#FF5252")
        self.clock_text.config(text=self._format_clock_text())
        self.root.after(1000, self.update_system_info)

    def run(self): self.root.mainloop()


if __name__ == "__main__":
    NexusBar().run()
