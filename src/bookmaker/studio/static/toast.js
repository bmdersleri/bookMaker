/* Toast notification system */
function showToast(msg, type) {
  type = type || 'info';
  var container = document.getElementById('toast-container');
  if (!container) return;
  var el = document.createElement('div');
  el.className = 'toast ' + type;
  el.innerHTML = '<span>' + msg + '</span><button class="close-toast" onclick="this.parentElement.remove()">&times;</button>';
  container.appendChild(el);
  setTimeout(function() { if (el.parentElement) el.remove(); }, 4000);
}
