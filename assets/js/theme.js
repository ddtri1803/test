(function(){
  const body = document.body;
  if(!body) return;

  const stateMap = {
    'pre-diagnosis': 'Pre-diagnosis / Trước chẩn đoán',
    'diagnosed': 'Diagnosed / Đã chẩn đoán',
    'active-treatment': 'Active treatment / Đang điều trị'
  };

  function applyState(state){
    body.dataset.state = state;

    document.querySelectorAll('[data-show]').forEach(el => {
      const allow = el.dataset.show.split(',').map(s=>s.trim());
      el.classList.toggle('hidden', !allow.includes(state));
    });

    document.querySelectorAll('[data-state-label]').forEach(el=>{
      el.textContent = stateMap[state] || state;
    });

    document.querySelectorAll('[data-set-state]').forEach(btn=>{
      btn.classList.toggle('active', btn.dataset.setState===state);
    });

    const step = body.dataset.step || 'diagnosis';
    const stepIndex = {diagnosis:1,plan:2,kit:3,monitoring:4}[step] || 1;
    document.querySelectorAll('[data-flow-step]').forEach((el, i)=>{
      el.classList.toggle('active', i+1===stepIndex);
    });
  }

  document.addEventListener('click', (e)=>{
    const btn = e.target.closest('[data-set-state]');
    if(!btn) return;
    applyState(btn.dataset.setState);
  });

  applyState(body.dataset.state || 'pre-diagnosis');
})();
