"""Fix: Tab button and add quality JS to app.js."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. FIX: Tab button in index.html
html_path = r'D:\bookMaker_Deepseek\src\bookmaker\studio\templates\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Find and fix the tabs div
if 'Yapilandirma' in html and 'Kalite' not in html:
    html = html.replace(
        '<button class="tab" data-tab="config" onclick="switchTab(\'config\')">Yapilandirma</button>\n</div>',
        '<button class="tab" data-tab="config" onclick="switchTab(\'config\')">Yapilandirma</button>\n'
        '  <button class="tab" data-tab="quality" onclick="loadQualityTab()">Kalite</button>\n</div>')
    print('OK: Kalite tab butonu eklendi')
else:
    print('Kalite tab butonu zaten var veya Yapilandirma bulunamadi')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

# 2. FIX: Add quality JS to app.js
js_path = r'D:\bookMaker_Deepseek\src\bookmaker\studio\static\app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

if 'loadQualityTab' not in js:
    quality_js = """

// =========== QUALITY PANEL ===========
let qualityData = [];
let qualitySortKey = 'score', qualitySortDir = 'desc';

async function loadQualityTab() {
  await loadQualityReport();
  await loadStats();
  await populateSearchChapters();
}
async function loadQualityReport() {
  const tb=document.getElementById('quality-body');
  if(!tb) return;
  try {
    const r=await fetch('/api/quality/report'); qualityData=await r.json();
    const sorted=[...qualityData].sort((a,b)=>(b.score||0)-(a.score||0));
    tb.innerHTML=sorted.map(function(d){
      if(d.error) return '<tr><td colspan=\"6\"><span class=\"tag danger\">'+escHtml(d.error)+'</span></td></tr>';
      var dc=d.decision==='pass'?'success':d.decision==='fail'?'danger':'warning';
      return '<tr><td><code>'+escHtml(d.chapter_id)+'</code></td><td><span class=\"tag '+scoreBadgeClass(d.score)+'\">'+d.score+'</span></td>'+
        '<td><span class=\"tag '+dc+'\">'+d.decision+'</span></td><td>'+(d.errors||0)+'</td><td>'+(d.warnings||0)+'</td>'+
        '<td><button class=\"btn btn-sm outline\" onclick=\"viewChapter(\''+d.chapter_id+'\')\">Gor</button></td></tr>';
    }).join('');
    document.getElementById('quality-table')?.classList.remove('hidden');
    document.getElementById('quality-loading')?.classList.add('hidden');
    var scores=qualityData.filter(function(d){return d.score!==undefined&&!d.error;});
    if(scores.length){
      var sum=scores.reduce(function(s,d){return s+d.score;},0);
      document.getElementById('quality-score-avg').textContent='Ort: '+Math.round(sum/scores.length);
    }
  } catch(e){}
}
async function loadStats() {
  try {
    var r=await fetch('/api/stats'); var d=await r.json();
    document.getElementById('stat-total-words').textContent=(d.total_words||0).toLocaleString();
    document.getElementById('stat-total-code').textContent=d.total_code_blocks||0;
    document.getElementById('stat-total-mermaid').textContent=d.total_mermaid||0;
    document.getElementById('stat-reading-time').textContent=(d.reading_minutes||0)+'dk';
    document.getElementById('stat-chapter-count').textContent=d.chapter_count||0;
    document.getElementById('stat-avg-words').textContent=(d.average_words||0).toLocaleString();
    var dist=document.getElementById('word-distribution');
    if(dist&&d.word_distribution&&d.word_distribution.length){
      var mw=0;
      for(var i=0;i<d.word_distribution.length;i++){if(d.word_distribution[i].words>mw) mw=d.word_distribution[i].words;}
      var html='<div style=\"font-size:.8rem;font-weight:600;color:var(--muted);margin-bottom:6px\">Kelime Dagitimi</div>';
      var slice=d.word_distribution.slice(0,10);
      for(var i=0;i<slice.length;i++){
        var w=slice[i];
        var pct=Math.max(2,(w.words/mw)*100);
        html+='<div style=\"display:flex;align-items:center;gap:8px;margin:3px 0;font-size:.78rem\">'+
          '<code style=\"min-width:80px\">'+escHtml(w.chapter_id)+'</code>'+
          '<div style=\"flex:1;height:16px;background:var(--border);border-radius:4px;overflow:hidden\">'+
          '<div style=\"height:100%;width:'+pct+'%;background:var(--primary);border-radius:4px\"></div></div>'+
          '<span style=\"min-width:50px;text-align:right;color:var(--muted)\">'+w.words.toLocaleString()+'</span></div>';
      }
      dist.innerHTML=html;
    }
  } catch(e){}
}
async function populateSearchChapters() {
  try {
    var r=await fetch('/api/chapters'); var chs=await r.json();
    var sel=document.getElementById('search-chapter');
    if(sel){
      sel.innerHTML='<option value=\"\">Tum Bolumler</option>';
      for(var i=0;i<chs.length;i++){
        sel.innerHTML+='<option value=\"'+chs[i].chapter_id+'\">'+escHtml(chs[i].chapter_id)+'</option>';
      }
    }
  } catch(e){}
}
async function runSearch() {
  var q=document.getElementById('search-query').value.trim();
  var chapter=document.getElementById('search-chapter').value;
  var regex=document.getElementById('search-regex').checked;
  var r=document.getElementById('search-results');
  if(!q){r.innerHTML='<div class=\"message info\">Arama kelimesi girin</div>';return;}
  r.innerHTML='<div class=\"message info\"><span class=\"spinner\"></span> Araniyor...</div>';
  try {
    var url='/api/search?q='+encodeURIComponent(q);
    if(chapter) url=url+'&chapter='+chapter;
    if(regex) url=url+'&regex=true';
    var resp=await fetch(url); var data=await resp.json();
    if(!data.length){r.innerHTML='<div class=\"message info\">Sonuc bulunamadi</div>';return;}
    r.innerHTML='';
    for(var i=0;i<Math.min(20,data.length);i++){
      var d=data[i];
      var ctx=d.context||d.text;
      if(ctx.length>300) ctx=ctx.slice(0,300);
      r.innerHTML+='<div style=\"margin:4px 0;padding:6px;background:#f9fafb;border-radius:4px\">'+
        '<div style=\"font-size:.75rem;color:var(--muted)\"><code>'+escHtml(d.chapter_id)+'</code> satir '+d.line+'</div>'+
        '<div style=\"font-size:.8rem;margin-top:2px\">'+escHtml(ctx)+'</div></div>';
    }
    if(data.length>20) r.innerHTML+='<div class=\"message info\">... ve '+(data.length-20)+' sonuc daha</div>';
  } catch(e){r.innerHTML='<div class=\"message error\">Hata: '+e.message+'</div>';}
}
"""

    # Insert before the BOOT event listener
    insert_before = 'document.addEventListener'
    idx = js.find(insert_before)
    if idx >= 0:
        js = js[:idx] + quality_js + '\n' + js[idx:]
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js)
        print('OK: Kalite JS eklendi (', len(quality_js), 'karakter)')
    else:
        print('HATA: Boot line bulunamadi')
else:
    print('Kalite JS zaten var')
