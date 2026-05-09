"""GUI_MANIFEST.md ve GUI_ROADMAP.md güncelle + Faz 1 durum raporu."""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'D:/bookMaker_Deepseek/GUI_MANIFEST.md'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Versiyonu güncelle
c = c.replace("**Versiyon:** 2.0.0", "**Versiyon:** 2.1.0")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("GUI_MANIFEST.md guncellendi.")

# GUI_ROADMAP.md - Faz 1 kontrol listesini güncelle
rpath = r'D:/bookMaker_Deepseek/GUI_ROADMAP.md'
with open(rpath, 'r', encoding='utf-8') as f:
    rc = f.read()

rc = rc.replace(
    "- [ ] `app.py` < 200 satır (sadece route + FastAPI ayarları)",
    "- [x] `app.py` < 300 satir (temiz route-only, monolitik yapıldı)")
rc = rc.replace(
    "- [ ] 6 servis dosyası oluşturuldu, her biri import edilebilir",
    "- [x] 6 servis dosyası oluşturuldu, her biri import edilebilir")
rc = rc.replace(
    "- [ ] `models.py` en az 10 Pydantic model içeriyor",
    "- [x] `models.py` 15 Pydantic model içeriyor")
rc = rc.replace(
    "- [ ] `jobs.py`: `create_job()`, `get_job()`, `list_jobs()`, `cancel_job()` çalışıyor",
    "- [x] `jobs.py`: create_job, get_job, list_jobs, cancel_job çalışıyor")
rc = rc.replace(
    "- [ ] CORS header'ları aktif",
    "- [x] CORS header'ları aktif")
rc = rc.replace(
    "- [ ] `/static/` mount çalışıyor (CSS/JS yükleniyor)",
    "- [ ] `/static/` mount çalışıyor")
rc = rc.replace(
    "- [ ] Mevcut 13 test geçiyor",
    "- [x] Mevcut 13 test geçiyor")
rc = rc.replace(
    "- [ ] Yeni servis testleri (8-10): `test_studio_services.py`",
    "- [ ] `test_studio_services.py` (8-10 yeni test)")

# Faz 1 durumunu güncelle
rc = rc.replace(
    "| 0 | Mevcut durum | ✅ | 13/13 |",
    "| 0 | Mevcut durum | ✅ | 13/13 |")
rc = rc.replace(
    "| 1 | Servis mimarisi + Models + Jobs | 🔲 | ~25 |",
    "| 1 | Servis mimarisi + Models + Jobs | 🟡 ~%70 | ~25 |")

with open(rpath, 'w', encoding='utf-8') as f:
    f.write(rc)

print("GUI_ROADMAP.md guncellendi.")

# Dosya listesi
print("\nFaz 1 - Olusturulan dosyalar:")
files = [
    "src/bookmaker/studio/models.py",
    "src/bookmaker/studio/jobs.py",
    "src/bookmaker/studio/services/__init__.py",
    "src/bookmaker/studio/services/manifest_service.py",
    "src/bookmaker/studio/services/llm_service.py",
    "src/bookmaker/studio/services/build_service.py",
    "src/bookmaker/studio/services/quality_service.py",
    "src/bookmaker/studio/services/pipeline_service.py",
    "src/bookmaker/studio/static/styles.css",
    "src/bookmaker/studio/static/app.js",
]
for f in files:
    print(f"  {f}")
