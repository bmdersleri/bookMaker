"""Faz 6: Build JS fonksiyonlarini app.js'e ekle."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

js_path = r'D:\bookMaker_Deepseek\src\bookmaker\studio\static\app.js'

with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

if 'runAssemble' in js:
    print('Build JS zaten var - atlaniyor')
    sys.exit(0)

build_js = r'''
// =========== BUILD PANEL ===========
var buildPanelInitialized = false;
function initBuildPanel() {
  if (buildPanelInitialized) return;
  buildPanelInitialized = true;
  fetch('/api/chapters').then(function(r){return r.json();}).then(function(chs){
    ['extract-chapter','mermaid-chapter'].forEach(function(id){
      var sel=document.getElementById(id);
      if(!sel) return;
      sel.innerHTML='<option value="">Tum Bolumler</option>'+chs.map(function(ch){
        return '<option value="'+ch.chapter_id+'">'+escHtml(ch.chapter_id)+'</option>';
      }).join('');
    });
  }).catch(function(){});
}

async function runExtractCode() {
  var cid=document.getElementById('extract-chapter').value;
  var el=document.getElementById('extract-result');
  el.innerHTML='<span class="spinner"></span> Kod cikariliyor...';
  try {
    var r=await fetch('/api/extract',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chapter_id:cid||null})});
    var d=await r.json();
    if(d.error){el.innerHTML='<div class="message error">'+escHtml(d.error)+'</div>';return;}
    el.innerHTML='<div class="message success">'+d.total_extracted+' kod blogu cikarildi -> '+escHtml(d.output_dir)+'</div>';
  } catch(e) { el.innerHTML='<div class="message error">'+e.message+'</div>'; }
}

async function runRenderMermaid() {
  var cid=document.getElementById('mermaid-chapter').value;
  var el=document.getElementById('mermaid-result');
  el.innerHTML='<span class="spinner"></span> Render ediliyor...';
  try {
    var r=await fetch('/api/render/mermaid',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chapter_id:cid||null})});
    var d=await r.json();
    if(d.error){el.innerHTML='<div class="message error">'+escHtml(d.error)+'</div>';return;}
    el.innerHTML='<div class="message success">'+d.rendered+' diyagram render edildi -> '+escHtml(d.output_dir)+'</div>';
  } catch(e) { el.innerHTML='<div class="message error">'+e.message+'</div>'; }
}

async function runAssemble() {
  var el=document.getElementById('export-result');
  el.innerHTML='<span class="spinner"></span> Birlestiriliyor...';
  try {
    var r=await fetch('/api/assemble',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
    var d=await r.json();
    if(d.error){el.innerHTML='<div class="message error">'+escHtml(d.error)+'</div>';return;}
    el.innerHTML='<div class="message success">'+d.chapters+' bolum, '+d.words+' kelime -> '+escHtml(d.path)+'</div>';
  } catch(e) { el.innerHTML='<div class="message error">'+e.message+'</div>'; }
}

async function runExport() {
  var fmt=document.getElementById('export-format').value;
  var el=document.getElementById('export-result');
  el.innerHTML='<span class="spinner"></span> Export ediliyor ('+fmt+')...';
  try {
    var r=await fetch('/api/export/'+fmt,{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
    var d=await r.json();
    if(d.error){el.innerHTML='<div class="message error">'+escHtml(d.error)+'</div>';return;}
    el.innerHTML='<div class="message success">'+fmt.toUpperCase()+' export tamam: '+escHtml(d.path)+' ('+d.size_bytes+' bytes)</div>';
  } catch(e) { el.innerHTML='<div class="message error">'+e.message+'</div>'; }
}

async function runBackup() {
  var el=document.getElementById('backup-result');
  el.innerHTML='<span class="spinner"></span> Yedekleniyor...';
  try {
    var r=await fetch('/api/backup',{method:'POST'});
    var d=await r.json();
    if(d.error){el.innerHTML='<div class="message error">'+escHtml(d.error)+'</div>';return;}
    el.innerHTML='<div class="message success">Yedek: '+escHtml(d.path)+' ('+d.size_mb+' MB, '+d.files+' dosya)</div>';
  } catch(e) { el.innerHTML='<div class="message error">'+e.message+'</div>'; }
}

// Tab switch override
var _origSwitchTab = switchTab;
switchTab = function(name) {
  if (name === 'build') initBuildPanel();
  _origSwitchTab(name);
};
'''

# Insert before last line
lines = js.split('\n')
insert_before = len(lines) - 1  # before last empty line
lines.insert(insert_before, build_js)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'Build JS eklendi: {len(build_js)} karakter')
