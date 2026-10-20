# 🦁 Nexus Bar

Windows için **sesli asistanlı, yapay zeka destekli, çok fonksiyonlu sistem çubuğu**.

Masaüstünün altında küçük bir çubuk olarak durur; CPU/RAM/disk/ağ/hava durumu gösterir,
Türkçe sesli komut dinler, Groq (Llama 3.1/3.3/4) ile soruları yanıtlar ve
telefonundan QR kod ile kontrol edilebilir.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/version-14.3-orange)

---

## ✨ Özellikler

### 🖥️ Sistem İzleme
- CPU, RAM, disk kullanımı (canlı bar grafikleri)
- Ağ indirme/yükleme hızı
- Sistem uptime
- İnternet bağlantı durumu (ON/OFF göstergesi)
- Pil / şarj durumu (sesli sorgu)
- Parlaklık göstergesi (fare tekerleği ile ayarlanabilir)

### 🌤️ Hava Durumu
- Otomatik konum tespiti (ip-api)
- 5 günlük tahmin (Open-Meteo, API anahtarı gerekmez)
- Animasyonlu detay paneli

### 🎤 Türkçe Sesli Asistan "Ahmet"
- `SpeechRecognition` + Google STT ile Türkçe komut dinleme
- `edge-tts` (tr-TR-AhmetNeural) ile doğal sesli yanıt
- **Çok katmanlı soru-cevap:**
  1. Öğretilen cevaplar (`nexus_qa.json`)
  2. Wikipedia (TR → EN)
  3. DuckDuckGo Instant Answer
  4. **Groq LLM** (Llama 3.1 8B, Llama 3.3 70B, Llama 4 Scout, Gemma2, Mixtral)
  5. Son çare: Google'da arama açar

### 📱 Telefondan Kontrol
- Yerel HTTP sunucu (port **8081**)
- QR kod ile bağlan → telefondan medya, ses, tema, ekran görüntüsü, kapatma
- Canlı "şu an çalıyor" kartı (albüm kapağı ile)
- Telefondan yapay zekaya soru sorma
- CPU/RAM göstergeleri

### 🎵 Medya Kontrolü
- Oynat / duraklat / sonraki / önceki
- Spotify / Windows Media Player açma-kapatma
- Şu an çalan şarkı + sanatçı + albüm kapağı (winsdk)
- Ses seviyesi yüzde ayarı (pycaw)

### 🧠 Yapay Zeka
- Groq API (ücretsiz katman)
- Birden fazla model otomatik deneme, çalışanı hatırlar
- Türkçe doğal cevaplar (max 3 cümle)
- Sesli okuma + bildirim

### 🛠️ Yardımcı Araçlar
- 🍅 Pomodoro zamanlayıcı (isteğe bağlı dakika)
- 💧 Su içme hatırlatıcısı (saatlik)
- ⏰ Alarm / hatırlatıcı
- 🧹 Geçici dosya + çöp kutusu temizleme
- 📷 Ekran görüntüsü (masaüstüne kaydeder)
- 📋 Görev yöneticisi lite (animasyonlu, işlem sonlandırma)
- 🔒 Windows kilitleme
- 🕶️ Gizlilik modu (Win+D)
- 🧮 Hesap makinesi (sesli "5 çarpı 3")
- 💱 Döviz kuru (Frankfurter API)
- 📰 Son haberler (TRT + AA RSS)
- 😄 Şaka / iltifat

### 🎨 Kişiselleştirme
- 4 tema: Koyu, Açık, Neon, Şeffaf
- Saydamlık ayarı
- 12/24 saat formatı
- Tarih gösterimi
- Profil fotoğrafı + isim
- Büyük saat modu (çift tıkla)
- Sürükle-bırak + kenara yapışma (snap)
- Pencere kilidi
- Her zaman üstte
- Sistem tepsisi ikonu

### 🚀 Ekstralar
- Otomatik başlatma (registry)
- `Ctrl+Shift+N` global kısayol
- Ayarlar `nexus_settings.json`'a kaydedilir
- Telegram/WhatsApp yok — hepsi tek dosya

---

## 📸 Ekran Görüntüleri

> _(Buraya kendi ekran görüntülerini ekle: çubuk, hava paneli, telefon kontrolü, QR kod vb.)_

---

## 🚀 Kurulum

### 1. Python gereksinimi
Python **3.10 veya üzeri** önerilir. Windows 10/11.

### 2. Depoyu indir
```bash
git clone https://github.com/kullaniciadi/nexus-bar.git
cd nexus-bar
```
Bağımlılıkları kur(hepsi)
```bash
pip install qrcode[pil] SpeechRecognition pyaudio edge-tts pygame pycaw comtypes winsdk
```
 derleme hatası verirse:
 ```bash
pip install pipwin
pipwin install pyaudio
```
Sesli komut örnekleri
```bash
"Ahmet, Einstein kimdir"
"Ahmet, hava nasıl"
"5 çarpı 7 kaç eder"
"Dolar kaç lira"
"Son haberleri oku"
"25 dakika pomodoro başlat"
"Müzik aç"
"Müziği duraklat"
"Ses yüzde 40"
"Ekran görüntüsü al"
"Bilgisayarı kilitle"
"Yapay zeka test et"
"Öğren Python bir programlama dili cevabı ..."
```
---

## 📌 Ek olarak eklemen gerekenler

1. **`.gitignore`** — mutlaka ekle:
```gitignore
__pycache__/
*.pyc
nexus_settings.json
nexus_qa.json
profile_image.png
.env
*.mp3
*.png
!docs/*.png
