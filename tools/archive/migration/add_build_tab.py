"""Faz 6: Build sekmesini frontend'e ekle."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'D:\bookMaker_Deepseek\src\bookmaker\studio\templates\index.html'
js_path = r'D:\bookMaker_Deepseek\src\bookmaker\studio\static\app.js'

# 1. Tab butonu ekle
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

if 'data-tab="build"' not in html:
    html = html.replace(
        '<button class="tab" data-tab="quality"',
        '<button class="tab" data-tab="build" onclick="switchTab(\'build\')">Build</button>\n  <button class="tab" data-tab="quality"')
    print('Build tab butonu eklendi')
else:
    print('Build tab butonu zaten var')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'index.html guncellendi: {len(html)} karakter')
