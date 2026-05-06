// ================================================================
// bookMaker Studio — app.js
// ================================================================
// STATE
let chapters = [], filteredChapters = [], projectData = {}, pipelineState = {};
let sortKey = 'order', sortDir = 'asc', filterStatus = 'all', searchQuery = '', currentPage = 1;
const PER_PAGE = 10;
let selectedIds = new Set();
let wsCancel = false;  // Flag to cancel pipeline

// INIT
async function init() { loadBookSelector(); await refreshAll(); await loadPipelineState(); await loadJobs(); }

// REFRESH
async function refreshAll() { await loadProject(); await loadChapters(); await loadLlmStatus(); }

// =========== BOOK SELECTOR DROPDOWN ===========
function loadBookSelector() {
  var sel = document.getElementById('book-selector');
  if (!sel) return;
  fetch('/api/projects').then(function(r){return r.json();}).then(function(projects){
    fetch('/api/active-book').then(function(r){return r.json();}).then(function(active){
      var currentPath = active.path || '';
      sel.innerHTML = projects.map(function(p){
        var selected = p.path === currentPath ? ' selected' : '';
        var label = typeof p.title === 'object' ? (p.title.tr || p.title.en || p.name) : (p.title||p.name);
        return '<option value="'+p.path.replace(/\\/g,'/')+'"'+selected+'>'+escHtml(label)+'</option>';
      }).join('');
      if (!projects.length) sel.innerHTML = '<option value="">Proje yok - once +Yeni Kitap ile olusturun</option>';
      updateBookHeader(active);
    }).catch(function(){
      sel.innerHTML = '<option value="">Aktif kitap alinamadi</option>';
    });
  }).catch(function(){
    sel.innerHTML = '<option value="">Projeler alinamadi</option>';
  });
}

function switchBook(path) {
  if (!path) return;
  var sel = document.getElementById('book-selector');
  sel.disabled = true;
  fetch('/api/active-book',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({path:path})})
    .then(function(r){return r.json();}).then(function(d){
      if (d.error) { showToast(d.error, 'error'); sel.disabled = false; loadBookSelector(); return; }
      showToast('Kitap degisti: ' + d.name, 'success');
      setTimeout(function(){ location.reload(); }, 400);
    }).catch(function(e){ showToast('Hata: ' + e.message, 'error'); sel.disabled = false; });
}

function updateBookHeader(active) {
  var el = document.getElementById('book-title');
  if (el && active && active.name) el.textContent = active.name || active.title || '';
}

// =========== STATS / PROJECT ===========
async function loadProject() {
  try {
    const r = await fetch('/api/project');
    projectData = await r.json();
    var bt = document.getElementById('book-title');
    if (bt) bt.textContent = projectData.title || '(isimsiz)';
    var el = document.getElementById('stat-chapters');
    if (el) el.textContent = projectData.chapters || 0;
    const sc = projectData.stage_counts || {};
    el = document.getElementById('stat-approved');
    if (el) el.textContent = (sc.approved || 0) + '/' + (projectData.chapters || 0);
    el = document.getElementById('stat-profile');
    if (el) el.textContent = projectData.profile || projectData.framework || '\u2014';
    el = document.getElementById('stat-code-language');
    if (el) el.textContent = projectData.code_language || '\u2014';
    el = document.getElementById('stat-stage');
    if (el) el.textContent = projectData.stage || '\u2014';
  } catch(e) { console.error('loadProject:', e); }
}

// =========== CHAPTERS ===========
function applyFilters() {
  let list = [...chapters];
  if (filterStatus !== 'all') list = list.filter(ch => ch.current_step === filterStatus);
  if (searchQuery.trim()) {
    const q = searchQuery.trim().toLowerCase();
    list = list.filter(ch => ch.chapter_id.toLowerCase().includes(q) || (ch.title||'').toLowerCase().includes(q));
  }
  list.sort((a,b) => {
    let va=a[sortKey], vb=b[sortKey];
    if (typeof va==='string') va=va.toLowerCase();
    if (typeof vb==='string') vb=vb.toLowerCase();
    return va < vb ? (sortDir==='asc'? -1 : 1) : va > vb ? (sortDir==='asc'? 1 : -1) : 0;
  });
  filteredChapters = list; currentPage = 1; renderTable(); renderPagination();
}
function setSort(key) {
  if (sortKey === key) sortDir = sortDir === 'asc' ? 'desc' : 'asc';
  else { sortKey = key; sortDir = 'asc'; }
  applyFilters();
}
function setFilter(status) { filterStatus = status; applyFilters(); }
function setSearch(q) { searchQuery = q; applyFilters(); }

function renderTable() {
  const tbody = document.getElementById('chapter-body');
  if (!tbody) return;
  const start = (currentPage-1)*PER_PAGE;
  const page = filteredChapters.slice(start, start+PER_PAGE);
  document.getElementById('chapter-count').textContent = filteredChapters.length;
  if (!page.length) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:2rem;color:#999">Bulunamadi</td></tr>'; return; }
  tbody.innerHTML = page.map(ch => {
    const sc = stepBadgeClass(ch.current_step), ss = scoreBadgeClass(ch.score);
    const sel = selectedIds.has(ch.chapter_id) ? 'checked' : '';
    return '<tr draggable="true" data-id="'+ch.chapter_id+'" class="chapter-row">'+
      '<td><input type="checkbox" class="chk-select" data-id="'+ch.chapter_id+'" '+sel+' onchange="toggleSelect(\''+ch.chapter_id+'\',this.checked)"></td>'+
      '<td class="drag-handle" title="Surukle-birak">&#x22EE;&#x22EE;</td>'+
      '<td><code>'+escHtml(ch.chapter_id)+'</code></td>'+
      '<td>'+escHtml(ch.title)+'</td>'+
      '<td><span class="tag '+sc+'">'+ch.current_step+'</span></td>'+
      '<td><span class="tag '+ss+'">'+ch.score+'</span></td>'+
      '<td><div class="action-group">'+
        '<button class="btn btn-sm outline" onclick="viewChapter(\''+ch.chapter_id+'\')">Gor</button>'+
        '<button class="btn btn-sm outline" onclick="checkChapter(\''+ch.chapter_id+'\')">Kontrol</button>'+
        '<button class="btn btn-sm outline" onclick="buildChapter(\''+ch.chapter_id+'\')">Build</button>'+
        '<button class="btn btn-sm primary" onclick="runPipeline(\''+ch.chapter_id+'\')">Uret</button>'+
      '</div></td></tr>';
  }).join('');
  // Drag
  document.querySelectorAll('.chapter-row').forEach(row => {
    row.addEventListener('dragstart', handleDragStart);
    row.addEventListener('dragover', handleDragOver);
    row.addEventListener('drop', handleDrop);
    row.addEventListener('dragend', handleDragEnd);
  });
}
function toggleSelect(id,c) { if(c) selectedIds.add(id); else selectedIds.delete(id); updateBulkButtons(); }
function selectAll(c) {
  const start=(currentPage-1)*PER_PAGE;
  filteredChapters.slice(start, start+PER_PAGE).forEach(ch => c ? selectedIds.add(ch.chapter_id) : selectedIds.delete(ch.chapter_id));
  renderTable(); updateBulkButtons();
}
function updateBulkButtons() {
  document.querySelectorAll('.bulk-only').forEach(el => el.style.display = selectedIds.size > 0 ? '' : 'none');
  document.getElementById('bulk-count').textContent = selectedIds.size;
}

// DRAG & DROP
let dragSrcId = null;
function handleDragStart(e) { dragSrcId=this.dataset.id; this.style.opacity='0.5'; e.dataTransfer.effectAllowed='move'; e.dataTransfer.setData('text/plain',dragSrcId); }
function handleDragOver(e) { e.preventDefault(); e.dataTransfer.dropEffect='move'; this.style.borderTop='2px solid #3a3a6e'; }
function handleDragEnd() { this.style.opacity='1'; document.querySelectorAll('.chapter-row').forEach(r=>r.style.borderTop=''); }
function handleDrop(e) {
  e.preventDefault();
  document.querySelectorAll('.chapter-row').forEach(r=>r.style.borderTop='');
  if (!dragSrcId || dragSrcId===this.dataset.id) return;
  const ids=filteredChapters.map(ch=>ch.chapter_id);
  const si=ids.indexOf(dragSrcId), ti=ids.indexOf(this.dataset.id);
  if (si===-1||ti===-1) return;
  ids.splice(si,1); ids.splice(ti,0,dragSrcId);
  fetch('/api/chapters/reorder',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({chapter_ids:ids})})
    .then(r=>r.json()).then(d=>{if(d.reordered){showToast('Siralama guncellendi','success');refreshAll();}})
    .catch(()=>showToast('Siralama kaydedilemedi','error'));
}

// PAGINATION
function renderPagination() {
  const el=document.getElementById('pagination'); if(!el) return;
  const t=Math.ceil(filteredChapters.length/PER_PAGE);
  if(t<=1){el.innerHTML='';return;}
  let h=''; if(currentPage>1) h+='<button class="btn btn-sm outline" onclick="goPage('+(currentPage-1)+')">&laquo;</button>';
  for(let i=1;i<=t;i++) h+='<button class="btn btn-sm '+(i===currentPage?'primary':'outline')+'" onclick="goPage('+i+')">'+i+'</button>';
  if(currentPage<t) h+='<button class="btn btn-sm outline" onclick="goPage('+(currentPage+1)+')">&raquo;</button>';
  el.innerHTML=h;
}
function goPage(p) { currentPage=p; renderTable(); renderPagination(); }

// BULK
async function bulkAction(action) {
  if(!selectedIds.size) return;
  showToast('Isleniyor: '+selectedIds.size+' bolum','info');
  const ids=Array.from(selectedIds);
  for(const id of ids) {
    if(action==='generate') await fetch('/api/generate/'+id,{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});
    else if(action==='build') await fetch('/api/build/'+id);
  }
  showToast(selectedIds.size+' bolum tamamlandi','success');
  selectedIds.clear(); updateBulkButtons(); await loadChapters();
}

// LOAD CHAPTERS
async function loadChapters() {
  const el=document.getElementById('chapter-loading'), er=document.getElementById('chapter-error'), tb=document.getElementById('chapter-table');
  if(el) el.classList.remove('hidden'); if(er) er.classList.add('hidden');
  try {
    const r=await fetch('/api/chapters'); chapters=await r.json(); applyFilters();
    if(el) el.classList.add('hidden'); if(tb) tb.classList.remove('hidden');
  } catch(e) { if(el) el.classList.add('hidden'); if(er){er.classList.remove('hidden');er.textContent='Yuklenemedi: '+e.message;} }
}

// JOBS
async function loadJobs() {
  try {
    const r=await fetch('/api/jobs'); const jobs=await r.json();
    const tb=document.getElementById('jobs-body'); if(!tb) return;
    if(!jobs.length) { tb.innerHTML='<tr><td colspan="5" style="text-align:center;color:#999">Henuz is yok</td></tr>'; return; }
    tb.innerHTML=jobs.slice(0,10).map(j=>'<tr><td><code>'+j.id.slice(0,8)+'</code></td><td>'+escHtml(j.chapter_id)+'</td><td>'+j.step+'</td><td><span class="tag '+jobStatusClass(j.status)+'">'+j.status+'</span></td><td>'+(j.elapsed_s?j.elapsed_s+'s':'-')+'</td></tr>').join('');
  } catch(e) {}
}
function jobStatusClass(s) { return {'queued':'neutral','running':'info','done':'success','error':'danger','cancelled':'warning'}[s]||'neutral'; }

// CHAPTER ACTIONS
async function viewChapter(id) {
  showModal('Goruntule: '+id,'<span class="spinner"></span> Yukleniyor...');
  try {
    const r=await fetch('/api/view/'+id); const d=await r.json();
    if(d.error){document.getElementById('modal-body').innerHTML='<div class="message error">'+escHtml(d.error)+'</div>';return;}
    document.getElementById('modal-body').innerHTML='<div style="font-size:.85rem;color:var(--muted);margin-bottom:1rem">'+d.path+' &middot; '+d.words.toLocaleString()+' kelime</div><div class="chapter-view">'+escHtml(d.full)+'</div>';
  } catch(e) { document.getElementById('modal-body').innerHTML='<div class="message error">Hata: '+e.message+'</div>'; }
}
async function checkChapter(id) {
  showModal('Kontrol: '+id,'<span class="spinner"></span> Kontrol ediliyor...');
  try {
    const r=await fetch('/api/check/'+id); const d=await r.json();
    if(d.error){document.getElementById('modal-body').innerHTML='<div class="message error">'+escHtml(d.error)+'</div>';return;}
    const dc=d.decision==='pass'?'success':d.decision==='fail'?'danger':'warning';
    document.getElementById('modal-body').innerHTML='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1rem">'+
      '<div class="stat-card"><div class="num">'+d.score+'</div><div class="lbl">Skor</div></div>'+
      '<div class="stat-card"><div class="num"><span class="tag '+dc+'">'+d.decision.toUpperCase()+'</span></div><div class="lbl">Karar</div></div>'+
      '<div class="stat-card"><div class="num" style="color:var(--danger)">'+d.errors+'</div><div class="lbl">Hata</div></div>'+
      '<div class="stat-card"><div class="num" style="color:var(--warning)">'+d.warnings+'</div><div class="lbl">Uyari</div></div></div>'+
      '<button class="btn outline" onclick="closeModal()">Kapat</button>';
  } catch(e) { document.getElementById('modal-body').innerHTML='<div class="message error">Hata: '+e.message+'</div>'; }
}
async function buildChapter(id) {
  showToast('Build ediliyor: '+id,'info');
  try {
    const r=await fetch('/api/build/'+id); const d=await r.json();
    showToast(d.error ? d.error : id+' build tamam: '+d.compiled+' kod', d.error?'error':'success');
  } catch(e) { showToast('Build hatasi: '+e.message,'error'); }
}
async function runPipeline(id) {
  document.getElementById('gen-chapter-id').value=id;
  document.getElementById('gen-title').value='';
  document.getElementById('gen-concepts').value='';
  switchTab('pipeline');
}

// =========== PIPELINE (Job Queue + Polling) ===========
function getEnrichTypes() {
  return Array.from(document.querySelectorAll('.chk-enrich:checked')).map(el=>el.value);
}

let _pollTimer = null;

async function runGeneration() {
  const id=document.getElementById('gen-chapter-id').value.trim();
  const title=document.getElementById('gen-title').value.trim();
  const conceptsRaw=document.getElementById('gen-concepts').value.trim();
  const output=document.getElementById('gen-output');
  const step=document.getElementById('gen-step'), bar=document.getElementById('gen-bar');
  const log=document.getElementById('gen-log');
  const cancelBtn=document.getElementById('cancel-pipeline-btn');

  if (!id) { showToast('Bolum ID gerekli', 'error'); return; }

  output.classList.remove('hidden');
  log.textContent = ''; bar.style.width = '5%';
  step.textContent = 'Is kuyruga ekleniyor...';
  cancelBtn.classList.remove('hidden');
  if (_pollTimer) clearInterval(_pollTimer);

  try {
    const r = await fetch('/api/generate/' + encodeURIComponent(id), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: title || undefined,
        concepts: conceptsRaw ? conceptsRaw.split(',').map(s => s.trim()) : undefined,
        enrich_types: getEnrichTypes()
      })
    });
    const data = await r.json();
    if (data.error) {
      step.textContent = 'HATA: ' + data.error;
      showToast(data.error, 'error');
      cancelBtn.classList.add('hidden');
      return;
    }

    const jobId = data.job_id;
    step.textContent = 'Is kuyrukta (# ' + jobId.slice(0,8) + ')...';
    log.textContent = 'Job ID: ' + jobId + '\n';

    const steps = { spec: 1, validate: 2, seed: 3, normalize: 4, enrich: 5, assemble: 6 };
    _pollTimer = setInterval(async () => {
      try {
        const jr = await fetch('/api/jobs/' + jobId);
        const job = await jr.json();
        if (!job || job.error) { clearInterval(_pollTimer); return; }

        const prog = job.progress || {};
        const done = steps[prog.current] || 0;
        bar.style.width = Math.min(95, (done / 6) * 100) + '%';
        step.textContent = '[' + (prog.current || '...') + '] ' + job.status;

        var logs = (prog.log || []);
        if (logs.length > 0) {
          log.textContent = 'Job: ' + jobId + '\n' + logs.slice(-8).join('\n');
        }

        if (job.status === 'done') {
          clearInterval(_pollTimer); _pollTimer = null;
          bar.style.width = '100%';
          var s = job.summary || {};
          step.textContent = 'Tamamlandi! ' + (s.words || '?') + ' kel, ' + (s.elapsed_s || '?') + 's';
          log.textContent += '\n\nDONE: ' + (s.words||'?') + ' kelime, ' + (s.elapsed_s||'?') + 's';
          cancelBtn.classList.add('hidden');
          showToast(id + ' uretildi: ' + (s.words||'?') + ' kel', 'success');
          loadChapters(); loadPipelineState(); loadJobs();
        } else if (job.status === 'error') {
          clearInterval(_pollTimer); _pollTimer = null;
          step.textContent = 'HATA';
          log.textContent += '\n\nHATA: ' + (job.error || 'Bilinmeyen hata');
          cancelBtn.classList.add('hidden');
          showToast('Pipeline hatasi: ' + (job.error || '?'), 'error');
        }
      } catch(e) { /* polling hatasi — devam */ }
    }, 2000);
  } catch(e) {
    step.textContent = 'HATA: ' + e.message;
    cancelBtn.classList.add('hidden');
  }
}

function cancelPipeline() {
  if (_pollTimer) { clearInterval(_pollTimer); _pollTimer = null; }
  document.getElementById('gen-step').textContent = 'Iptal edildi';
  document.getElementById('cancel-pipeline-btn').classList.add('hidden');
  showToast('Pipeline iptal edildi', 'info');
}

// =========== LLM CONFIG ===========
function showLlmConfig() { switchTab('config'); }
async function loadLlmStatus() {
  try {
    const r=await fetch('/api/llm-status'); const d=await r.json();
    const el=document.getElementById('stat-llm');
    el.textContent=d.configured?d.model:'Ayarlanmamis';
    el.style.color=d.configured?'var(--success)':'var(--danger)';
    document.getElementById('llm-current').innerHTML=d.configured?'<span class="status-dot green"></span> '+d.provider+' / '+d.model:'<span class="status-dot red"></span> Yapilandirilmamis';
    document.getElementById('llm-provider').value=d.provider||'deepseek';
    document.getElementById('llm-model').value=d.model||'deepseek-chat';
  } catch(e) {}
}
async function saveLlmConfig() {
  const provider=document.getElementById('llm-provider').value, api_key=document.getElementById('llm-key').value.trim(), model=document.getElementById('llm-model').value.trim();
  if(!api_key){showToast('API anahtari gerekli','error');return;}
  try {
    const r=await fetch('/api/llm-configure',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({provider,api_key,model})});
    const d=await r.json();
    if(d.error) showToast(d.error,'error');
    else { document.getElementById('llm-key').value=''; showToast('LLM yapilandirildi','success'); await loadLlmStatus(); }
  } catch(e) { showToast('Kaydedilemedi: '+e.message,'error'); }
}
async function testLlmConnection() {
  const el=document.getElementById('llm-test-result');
  el.classList.remove('hidden');
  el.innerHTML='<span class="spinner"></span> Test ediliyor...';
  try {
    const r=await fetch('/api/llm-test'); const d=await r.json();
    el.innerHTML=d.status==='ok'?'<div class="message success">Baglanti basarili: '+d.model+'</div>':'<div class="message error">'+d.message+'</div>';
  } catch(e) { el.innerHTML='<div class="message error">'+e.message+'</div>'; }
}
async function loadPipelineState() {
  try {
    const r=await fetch('/api/pipeline-state'); pipelineState=await r.json();
    const el=document.getElementById('pipeline-state-view');
    if(el) el.textContent=JSON.stringify(pipelineState,null,2);
  } catch(e) { const el=document.getElementById('pipeline-state-view'); if(el) el.textContent='Yuklenemedi: '+e.message; }
}
async function showAllPipeline() { switchTab('pipeline'); await loadPipelineState(); await loadJobs(); }

// =========== TABS / MODAL / HELPERS ===========
function switchTab(name) {
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
  var at=document.querySelector('.tab[data-tab="'+name+'"]'); if(at) at.classList.add('active');
  var ac=document.getElementById('tab-'+name); if(ac) ac.classList.add('active');
  var loaders = {
    chapters: loadChapters,
    pipeline: async function() { await loadPipelineState(); await loadJobs(); },
    config: loadLlmStatus,
    quality: loadQualityTab,
    build: initBuildPanel,
    prompts: loadPromptTab
  };
  var loader = loaders[name];
  if (loader) {
    Promise.resolve(loader()).catch(function(e) {
      console.error('Tab load failed:', name, e);
      showToast(name + ' sekmesi yuklenemedi: ' + e.message, 'error');
    });
  }
}
function showModal(title,bodyHtml) {
  document.getElementById('modal-title').textContent=title;
  document.getElementById('modal-body').innerHTML=bodyHtml;
  document.getElementById('modal-overlay').classList.remove('hidden');
}
function closeModal(e) { if(e&&e.target!==e.currentTarget) return; document.getElementById('modal-overlay').classList.add('hidden'); }
function escHtml(s) { if(!s) return ''; var d=document.createElement('div'); d.textContent=s; return d.innerHTML; }

// =========== BOOK LOADER ===========
function showBookLoader() {
  document.getElementById('book-loader').classList.remove('hidden');
  var el=document.getElementById('book-list');
  el.innerHTML='<span class="spinner"></span> Projeler taranıyor...';
  fetch('/api/projects').then(function(r){return r.json();}).then(function(projects){
    if(!projects.length){el.innerHTML='<div class="message info">Henuz proje yok</div>';return;}
    fetch('/api/active-book').then(function(r){return r.json();}).then(function(active){
      var currentPath=active.path||'';
      el.innerHTML='<div style="margin-bottom:1rem;font-size:.78rem;color:var(--muted)">Bir kitap projesi secin:</div>'+
        '<div style="display:flex;flex-direction:column;gap:4px">'+
        projects.map(function(p){
          var isActive=p.path===currentPath;
          var title=p.title||p.name;
          return '<div style="display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:6px;cursor:pointer;'+
            (isActive?'background:var(--primary);color:#fff':'background:#f9fafb')+
            '" onclick="setActiveBook(\''+p.path.replace(/\\\\/g,'/')+'\',this)">'+
            '<span style="font-size:1.1rem">'+(isActive?'📚':'📖')+'</span>'+
            '<div><strong>'+escHtml(title)+'</strong><br><span style="font-size:.75rem;opacity:.7">'+escHtml(p.name)+'</span></div>'+
            (isActive?'<span style="margin-left:auto;font-size:.75rem">Aktif</span>':'')+
            '</div>';
        }).join('')+
        '</div>';
    }).catch(function(){el.innerHTML='<div class="message error">Aktif kitap bilgisi alinamadi</div>';});
  }).catch(function(){el.innerHTML='<div class="message error">Projeler listelenemedi</div>';});
}

function closeBookLoader(e) {
  if(e&&e.target!==e.currentTarget)return;
  document.getElementById('book-loader').classList.add('hidden');
}

function setActiveBook(path,el) {
  fetch('/api/active-book',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({path:path})})
    .then(function(r){return r.json();}).then(function(d){
      if(d.error){showToast(d.error,'error');return;}
      showToast('Kitap degisti: '+d.name,'success');
      closeBookLoader();
      refreshAll();
      setTimeout(function(){location.reload();},500);
    }).catch(function(e){showToast('Hata: '+e.message,'error');});
}

// =========== WIZARD ===========
var wizStep=1,wizChapters=[];
function openWizard(){
  wizStep=1;
  wizChapters=[];
  document.getElementById('wizard-overlay').classList.remove('hidden');
  document.getElementById('wiz-project').value='book-'+Date.now().toString(36);
  document.getElementById('wiz-title').value='';
  document.getElementById('wiz-author').value='';
  document.getElementById('wiz-chapters').value='';
  document.getElementById('wiz-plan-table').innerHTML='';
  updateWizard();
}
function closeWizard(e){if(e&&e.target!==e.currentTarget)return;document.getElementById('wizard-overlay').classList.add('hidden');}

function updateWizard(){
  document.querySelectorAll('.wiz-step').forEach(function(s){s.classList.toggle('active',parseInt(s.dataset.step)===wizStep);});
  document.querySelectorAll('.wiz-panel').forEach(function(p){p.classList.toggle('hidden',parseInt(p.dataset.step)!==wizStep);});
  document.getElementById('wiz-prev').style.display=wizStep>1?'':'none';
  document.getElementById('wiz-next').textContent=wizStep===3?'Kitabi Olustur':'Ilerle';
  setWizardError('');
  if(wizStep===3) updateSummary();
}
function setWizardError(message){
  var err=document.getElementById('wiz-err');
  if(!err) return;
  err.textContent=message||'';
  err.classList.toggle('hidden',!message);
}
function validateStep(n){
  if(n===1){
    if(!document.getElementById('wiz-project').value.trim()){setWizardError('Proje adi gerekli');return false;}
    if(!document.getElementById('wiz-title').value.trim()){setWizardError('Kitap adi gerekli');return false;}
    if(!document.getElementById('wiz-author').value.trim()){setWizardError('Yazar gerekli');return false;}
  }
  if(n===2){
    parseWizardChapters();
    if(!wizChapters.length){setWizardError('En az 1 bolum ekleyin');return false;}
  }
  return true;
}
function nextWiz(){
  if(!validateStep(wizStep)) return;
  if(wizStep===3){submitWizard();return;}
  wizStep++;updateWizard();
}
function prevStep(){if(wizStep>1){wizStep--;updateWizard();}}
function wizValidate(n){validateStep(n);}
function nextStep(){ nextWiz(); }

function parseWizardChapters(){
  var raw=document.getElementById('wiz-chapters').value.split(/\r?\n/);
  wizChapters=[];
  raw.forEach(function(line){
    var text=line.trim();
    if(!text) return;
    var parts=text.split(':');
    var alias=parts.shift().trim();
    var title=(parts.join(':').trim()||alias);
    if(alias) wizChapters.push({alias:alias,chapter_id:alias,title:title,type:'core'});
  });
  return wizChapters;
}
function initManualPlan(){
  var count=parseInt(document.getElementById('wiz-chapter-count').value)||23;
  var appendix=parseInt(document.getElementById('wiz-appendix-count').value)||4;
  wizChapters=[];
  for(var i=1;i<=count;i++) wizChapters.push({alias:'bolum-'+String(i).padStart(2,'0'),chapter_id:'bolum-'+String(i).padStart(2,'0'),title:'Bolum '+i,type:'core'});
  for(var j=0;j<appendix;j++) wizChapters.push({alias:'ek-'+'abcdefghijklmnop'[j],chapter_id:'ek-'+'abcdefghijklmnop'[j],title:'Ek '+String.fromCharCode(65+j),type:'appendix'});
  document.getElementById('wiz-chapters').value=wizChapters.map(function(ch){return ch.alias+': '+ch.title;}).join('\n');
  renderPlanTable();
  showToast(count+appendix+' bolum olusturuldu','success');
}
function renderPlanTable(){
  var el=document.getElementById('wiz-plan-table');
  if(!wizChapters.length){el.innerHTML='<div class="message info">Plan bos</div>';return;}
  el.innerHTML='<table><thead><tr><th>ID</th><th>Baslik</th><th>Tur</th><th></th></tr></thead><tbody>'+
    wizChapters.map(function(ch,i){return '<tr><td><code>'+escHtml(ch.alias||ch.chapter_id)+'</code></td><td><input type="text" value="'+escHtml(ch.title||'')+'" style="width:100%;border:none;border-bottom:1px solid var(--border);padding:2px 4px;font-size:.82rem" onchange="wizChapters['+i+'].title=this.value;syncWizardChapterText()"></td><td>'+ch.type+'</td><td><button class="btn btn-sm danger" onclick="wizChapters.splice('+i+',1);syncWizardChapterText();renderPlanTable()">X</button></td></tr>';}).join('')+
    '</tbody></table>';
}
function syncWizardChapterText(){
  document.getElementById('wiz-chapters').value=wizChapters.map(function(ch){return (ch.alias||ch.chapter_id)+': '+(ch.title||ch.alias||ch.chapter_id);}).join('\n');
}
function updateSummary(){
  var el=document.getElementById('wiz-summary');
  parseWizardChapters();
  var core=wizChapters.filter(function(c){return c.type==='core';}).length;
  var appx=wizChapters.filter(function(c){return c.type!=='core';}).length;
  el.innerHTML='<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem">'+
    '<div class="stat-card"><div class="num">'+escHtml(document.getElementById('wiz-project').value)+'</div><div class="lbl">Proje</div></div>'+
    '<div class="stat-card"><div class="num">'+core+'+'+appx+'</div><div class="lbl">Bolum</div></div>'+
    '<div class="stat-card"><div class="num">'+escHtml(document.getElementById('wiz-title').value)+'</div><div class="lbl">Kitap</div></div>'+
    '<div class="stat-card"><div class="num">'+escHtml(document.getElementById('wiz-author').value)+'</div><div class="lbl">Yazar</div></div></div>'+
    '<div style="font-size:.82rem;color:var(--muted)">Olusturulacak dosyalar:<br>book_manifest.yaml, pipeline_state.yaml, prompts/, chapters/&lt;alias&gt;/chapter_manifest.yaml, content/draft.md, content/final.md</div>';
}
async function submitWizard(){
  var btn=document.getElementById('wiz-next');btn.disabled=true;btn.textContent='Olusturuluyor...';
  try{
    var r=await fetch('/api/book/create',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
      project_name:document.getElementById('wiz-project').value.trim(),
      title:document.getElementById('wiz-title').value.trim(),
      author:document.getElementById('wiz-author').value.trim(),
      audience:document.getElementById('wiz-audience').value,
      language:document.getElementById('wiz-language').value,
      book_type:document.getElementById('wiz-book-type').value,
      chapter_count:parseInt(document.getElementById('wiz-chapter-count').value)||5,
      appendix_count:parseInt(document.getElementById('wiz-appendix-count').value)||0,
      chapters:wizChapters.map(function(ch){return {alias:ch.alias||ch.chapter_id,title:ch.title||ch.alias||ch.chapter_id};})
    })});
    var d=await r.json();
    if(d.error){showToast(d.error,'error');setWizardError(d.error);btn.disabled=false;btn.textContent='Kitabi Olustur';return;}
    showToast('Kitap olusturuldu: '+d.title,'success');
    closeWizard();
    await loadBookSelector();
    await refreshAll();
  }catch(e){showToast('Hata: '+e.message,'error');setWizardError(e.message);}
  finally{btn.disabled=false;btn.textContent='Kitabi Olustur';}
}

function stepBadgeClass(s) { return {'approved':'success','full_text_pasted':'success','enriched':'info','seed':'info','outline':'warning','planned':'neutral'}[s]||'neutral'; }
function scoreBadgeClass(s) { return s>=80?'score-high':s>=50?'tag-score-mid':'score-low'; }
function showToast(msg,type) {
  var c=document.getElementById('toast-container'); if(!c) return;
  var el=document.createElement('div'); el.className='toast '+(type||'info');
  el.innerHTML='<span>'+escHtml(msg)+'</span><button class="close-toast" onclick="this.parentElement.remove()">&times;</button>';
  c.appendChild(el); setTimeout(function(){if(el.parentElement)el.remove();},4000);
}

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
      if(d.error) return '<tr><td colspan="6"><span class="tag danger">'+escHtml(d.error)+'</span></td></tr>';
      var dc=d.decision==='pass'?'success':d.decision==='fail'?'danger':'warning';
      return '<tr><td><code>'+escHtml(d.chapter_id)+'</code></td><td><span class="tag '+scoreBadgeClass(d.score)+'">'+d.score+'</span></td>'+
        '<td><span class="tag '+dc+'">'+d.decision+'</span></td><td>'+(d.errors||0)+'</td><td>'+(d.warnings||0)+'</td>'+
        '<td><button class="btn btn-sm outline" onclick="viewChapter(\''+d.chapter_id+'\')">Gor</button></td></tr>';
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
      var html='<div style="font-size:.8rem;font-weight:600;color:var(--muted);margin-bottom:6px">Kelime Dagitimi</div>';
      var slice=d.word_distribution.slice(0,10);
      for(var i=0;i<slice.length;i++){
        var w=slice[i];
        var pct=Math.max(2,(w.words/mw)*100);
        html+='<div style="display:flex;align-items:center;gap:8px;margin:3px 0;font-size:.78rem">'+
          '<code style="min-width:80px">'+escHtml(w.chapter_id)+'</code>'+
          '<div style="flex:1;height:16px;background:var(--border);border-radius:4px;overflow:hidden">'+
          '<div style="height:100%;width:'+pct+'%;background:var(--primary);border-radius:4px"></div></div>'+
          '<span style="min-width:50px;text-align:right;color:var(--muted)">'+w.words.toLocaleString()+'</span></div>';
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
      sel.innerHTML='<option value="">Tum Bolumler</option>';
      for(var i=0;i<chs.length;i++){
        sel.innerHTML+='<option value="'+chs[i].chapter_id+'">'+escHtml(chs[i].chapter_id)+'</option>';
      }
    }
  } catch(e){}
}
async function runSearch() {
  var q=document.getElementById('search-query').value.trim();
  var chapter=document.getElementById('search-chapter').value;
  var regex=document.getElementById('search-regex').checked;
  var r=document.getElementById('search-results');
  if(!q){r.innerHTML='<div class="message info">Arama kelimesi girin</div>';return;}
  r.innerHTML='<div class="message info"><span class="spinner"></span> Araniyor...</div>';
  try {
    var url='/api/search?q='+encodeURIComponent(q);
    if(chapter) url=url+'&chapter='+chapter;
    if(regex) url=url+'&regex=true';
    var resp=await fetch(url); var data=await resp.json();
    if(!data.length){r.innerHTML='<div class="message info">Sonuc bulunamadi</div>';return;}
    r.innerHTML='';
    for(var i=0;i<Math.min(20,data.length);i++){
      var d=data[i];
      var ctx=d.context||d.text;
      if(ctx.length>300) ctx=ctx.slice(0,300);
      r.innerHTML+='<div style="margin:4px 0;padding:6px;background:#f9fafb;border-radius:4px">'+
        '<div style="font-size:.75rem;color:var(--muted)"><code>'+escHtml(d.chapter_id)+'</code> satir '+d.line+'</div>'+
        '<div style="font-size:.8rem;margin-top:2px">'+escHtml(ctx)+'</div></div>';
    }
    if(data.length>20) r.innerHTML+='<div class="message info">... ve '+(data.length-20)+' sonuc daha</div>';
  } catch(e){r.innerHTML='<div class="message error">Hata: '+e.message+'</div>';}
}

// =========== PROMPT PANEL ===========
let currentPromptEndpoint = null;
let promptDirty = false;

function selectedPromptEndpoint() {
  var scope = document.getElementById('prompt-scope')?.value || 'default_chapter';
  if (scope === 'default_review') return '/api/prompts/default/review';
  if (scope === 'chapter') {
    var chapter = document.getElementById('prompt-chapter')?.value;
    return chapter ? '/api/prompts/chapter/' + encodeURIComponent(chapter) : null;
  }
  return '/api/prompts/default/chapter';
}

async function loadPromptTab() {
  await populatePromptChapters();
  updatePromptControls();
  if (!currentPromptEndpoint) await loadSelectedPrompt();
}

async function populatePromptChapters() {
  var sel = document.getElementById('prompt-chapter');
  if (!sel) return;
  var source = chapters;
  if (!source.length) {
    try {
      var r = await fetch('/api/chapters');
      source = await r.json();
    } catch(e) {
      source = [];
    }
  }
  sel.innerHTML = source.map(function(ch) {
    var title = ch.title ? ' - ' + ch.title : '';
    return '<option value="' + escHtml(ch.chapter_id) + '">' +
      escHtml(ch.chapter_id + title) + '</option>';
  }).join('');
}

function updatePromptControls() {
  var scope = document.getElementById('prompt-scope')?.value || 'default_chapter';
  var chapter = document.getElementById('prompt-chapter');
  if (chapter) chapter.classList.toggle('hidden', scope !== 'chapter');
}

function showPromptMessage(message, type) {
  var el = document.getElementById('prompt-message');
  if (!el) return;
  el.className = 'message ' + (type || 'info');
  el.textContent = message;
  el.classList.remove('hidden');
}

function markPromptDirty() {
  promptDirty = true;
  var btn = document.getElementById('prompt-save');
  if (btn && currentPromptEndpoint) btn.disabled = false;
}

async function loadSelectedPrompt() {
  var endpoint = selectedPromptEndpoint();
  var editor = document.getElementById('prompt-editor');
  var path = document.getElementById('prompt-path');
  var save = document.getElementById('prompt-save');
  if (!endpoint || !editor) {
    showPromptMessage('Once bir bolum secin.', 'warning');
    return;
  }
  editor.disabled = true;
  showPromptMessage('Prompt yukleniyor...', 'info');
  try {
    var r = await fetch(endpoint);
    var data = await r.json();
    if (data.error) {
      showPromptMessage(data.error, 'error');
      return;
    }
    currentPromptEndpoint = endpoint;
    editor.value = data.content || '';
    editor.disabled = false;
    promptDirty = false;
    if (save) save.disabled = true;
    if (path) path.textContent = data.path || '-';
    showPromptMessage('Prompt yuklendi.', 'success');
  } catch(e) {
    showPromptMessage('Prompt yuklenemedi: ' + e.message, 'error');
  } finally {
    editor.disabled = false;
  }
}

async function saveSelectedPrompt() {
  var endpoint = currentPromptEndpoint || selectedPromptEndpoint();
  var editor = document.getElementById('prompt-editor');
  var save = document.getElementById('prompt-save');
  if (!endpoint || !editor) {
    showPromptMessage('Kaydedilecek prompt yok.', 'warning');
    return;
  }
  if (save) save.disabled = true;
  try {
    var r = await fetch(endpoint, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({content: editor.value})
    });
    var data = await r.json();
    if (data.error) {
      showPromptMessage(data.error, 'error');
      if (save) save.disabled = false;
      return;
    }
    promptDirty = false;
    if (document.getElementById('prompt-path')) {
      document.getElementById('prompt-path').textContent = data.path || '-';
    }
    showPromptMessage('Prompt kaydedildi.', 'success');
    showToast('Prompt kaydedildi', 'success');
  } catch(e) {
    showPromptMessage('Prompt kaydedilemedi: ' + e.message, 'error');
    if (save) save.disabled = false;
  }
}

document.addEventListener('DOMContentLoaded', init);

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
    var r=await fetch('/api/extract/code',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chapter_id:cid||null})});
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
    var html='<div class="message success">'+d.rendered+' diyagram render edildi -> '+escHtml(d.output_dir)+'</div>';
    if(d.images && d.images.length>0){
      html+='<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px">';
      for(var i=0;i<d.images.length;i++){
        html+='<div style="border:1px solid var(--border);border-radius:6px;padding:4px;background:#fff"><img src="/output/'+escHtml(d.images[i])+'" style="max-width:200px;max-height:150px" alt="diagram" onerror="this.parentElement.style.display=\'none\'"></div>';
      }
      html+='</div>';
    }
    if(d.errors && d.errors.length>0){
      html+='<div class="message warning" style="margin-top:4px">'+d.errors.map(escHtml).join('<br>')+'</div>';
    }
    el.innerHTML=html;
  } catch(e) { el.innerHTML='<div class="message error">'+e.message+'</div>'; }
}

async function runAssemble() {
  var el=document.getElementById('export-result');
  el.innerHTML='<span class="spinner"></span> Birlestiriliyor...';
  try {
    var r=await fetch('/api/assemble',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({})});
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
    var r=await fetch('/api/export/'+fmt,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({})});
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
    var rip=document.getElementById('restore-path');
    if(rip && d.path) rip.value=d.path;
    el.innerHTML='<div class="message success">Yedek: '+escHtml(d.path)+' ('+d.size_mb+' MB, '+d.files+' dosya)</div>';
  } catch(e) { el.innerHTML='<div class="message error">'+e.message+'</div>'; }
}

async function runRestore() {
  var el=document.getElementById('backup-result');
  var rip=document.getElementById('restore-path');
  var path=rip?rip.value:'';
  if(!path){el.innerHTML='<div class="message error">Yedek dosya yolu girin</div>';return;}
  el.innerHTML='<span class="spinner"></span> Geri yukleniyor...';
  try {
    var r=await fetch('/api/restore',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({path:path})});
    var d=await r.json();
    if(d.error){el.innerHTML='<div class="message error">'+escHtml(d.error)+'</div>';return;}
    el.innerHTML='<div class="message success">Geri yuklendi: '+d.files+' dosya</div>';
    showToast('Yedek geri yuklendi: '+d.files+' dosya','success');
  } catch(e) { el.innerHTML='<div class="message error">'+e.message+'</div>'; }
}

async function runIndex() {
  var el=document.getElementById('index-result');
  el.innerHTML='<span class="spinner"></span> Indeks olusturuluyor...';
  try {
    var r=await fetch('/api/index',{method:'POST'});
    var d=await r.json();
    if(d.error){el.innerHTML='<div class="message error">'+escHtml(d.error)+'</div>';return;}
    el.innerHTML='<div class="message success">Indeks: '+d.entries+' baslik, '+d.chapters_indexed+' bolum -> '+escHtml(d.path)+'</div>';
  } catch(e) { el.innerHTML='<div class="message error">'+e.message+'</div>'; }
}

async function runGlossary() {
  var el=document.getElementById('index-result');
  el.innerHTML='<span class="spinner"></span> Glossary olusturuluyor...';
  try {
    var r=await fetch('/api/glossary',{method:'POST'});
    var d=await r.json();
    if(d.error){el.innerHTML='<div class="message error">'+escHtml(d.error)+'</div>';return;}
    el.innerHTML='<div class="message success">Glossary: '+d.terms+' terim -> '+escHtml(d.path)+'</div>';
  } catch(e) { el.innerHTML='<div class="message error">'+e.message+'</div>'; }
}

