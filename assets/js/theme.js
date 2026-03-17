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
    document.querySelectorAll('[data-state-label]').forEach(el=>el.textContent = stateMap[state] || state);
    document.querySelectorAll('[data-set-state]').forEach(btn=>btn.classList.toggle('active', btn.dataset.setState===state));
    const stepIndex = {diagnosis:1,plan:2,kit:3,monitoring:4}[body.dataset.step || 'diagnosis'] || 1;
    document.querySelectorAll('[data-flow-step]').forEach((el, i)=>el.classList.toggle('active', i+1===stepIndex));
  }

  document.addEventListener('click', (e)=>{
    const stateBtn = e.target.closest('[data-set-state]');
    if(stateBtn) applyState(stateBtn.dataset.setState);

    const phaseBtn = e.target.closest('[data-phase-target]');
    if(phaseBtn){
      const id = phaseBtn.dataset.phaseTarget;
      document.querySelectorAll('[data-phase-target]').forEach(b=>b.classList.remove('active'));
      phaseBtn.classList.add('active');
      document.querySelectorAll('[data-phase-panel]').forEach(p=>p.classList.add('hidden'));
      const panel = document.querySelector(`[data-phase-panel="${id}"]`);
      if(panel) panel.classList.remove('hidden');
    }

    const roleBtn = e.target.closest('[data-role-target]');
    if(roleBtn){
      const id = roleBtn.dataset.roleTarget;
      const item = roleBtn.closest('.role-item');
      item.classList.toggle('open');
      const panel = document.querySelector(`[data-role-panel="${id}"]`);
      if(panel) panel.classList.toggle('hidden');
    }

    const riskBtn = e.target.closest('[data-risk]');
    if(riskBtn){
      const output = document.querySelector('[data-risk-output]');
      const map = {
        skip_phase1: ['Skipping repair raises irritation risk.', 'Bỏ qua phase phục hồi làm tăng nguy cơ kích ứng.'],
        swap_active: ['Random active swap can trigger flare-ups.', 'Đổi hoạt chất ngẫu nhiên có thể gây bùng viêm.'],
        stop_spf: ['Stopping SPF increases relapse and pigmentation.', 'Ngưng chống nắng làm tăng tái phát và tăng sắc tố.']
      };
      const [en, vi] = map[riskBtn.dataset.risk] || ['Follow assigned protocol.', 'Hãy tuân thủ đúng phác đồ.'];
      if(output) output.innerHTML = `<strong>${en}</strong><br><span class="text-slate-600">${vi}</span>`;
    }

    const quick = e.target.closest('[data-chat-reply]');
    if(quick){
      addChatBubble(quick.textContent.trim(), 'user');
      quick.closest('[data-chat-options]').classList.add('hidden');
      const next = quick.dataset.chatReply;
      runChatStep(next);
    }
  });

  function initQuiz(){
    const wrap = document.querySelector('[data-quiz]');
    if(!wrap) return;
    const steps = [...wrap.querySelectorAll('[data-quiz-step]')];
    const nextBtn = wrap.querySelector('[data-quiz-next]');
    const prevBtn = wrap.querySelector('[data-quiz-prev]');
    const progress = wrap.querySelector('[data-quiz-progress]');
    const summary = wrap.querySelector('[data-quiz-summary]');
    let idx = 0;

    const showStep = () => {
      steps.forEach((s,i)=>s.classList.toggle('hidden', i!==idx));
      prevBtn.classList.toggle('hidden', idx===0);
      nextBtn.textContent = idx===steps.length-1 ? 'Finish Quiz' : 'Next Question';
      if(progress) progress.style.width = `${((idx+1)/steps.length)*100}%`;
    };

    steps.forEach(step=>{
      step.querySelectorAll('.quiz-answer').forEach(btn=>{
        btn.addEventListener('click', ()=>{
          step.querySelectorAll('.quiz-answer').forEach(b=>b.classList.remove('selected'));
          btn.classList.add('selected');
          step.dataset.answer = btn.dataset.value;
        });
      });
    });

    nextBtn?.addEventListener('click', ()=>{
      if(!steps[idx].dataset.answer) return;
      if(idx<steps.length-1){ idx++; showStep(); return; }
      const answers = steps.map(s=>s.dataset.answer || '-');
      summary.classList.remove('hidden');
      summary.innerHTML = `<p class="bi-en">Profile detected: ${answers.join(' • ')}</p><p class="bi-vi">Hồ sơ da ghi nhận: ${answers.join(' • ')}</p>`;
      wrap.classList.add('hidden');
      document.querySelector('[data-after-quiz]')?.classList.remove('hidden');
    });

    prevBtn?.addEventListener('click', ()=>{ if(idx>0){ idx--; showStep(); } });
    showStep();
  }

  function addChatBubble(text, who){
    const log = document.querySelector('[data-chat-log]');
    if(!log) return;
    const div = document.createElement('div');
    div.className = who==='user' ? 'chat-bubble-user' : 'chat-bubble-bot';
    div.textContent = text;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
  }

  function runChatStep(step){
    const map = {
      start: {bot:'How soon do you want to begin treatment? / Bạn muốn bắt đầu điều trị khi nào?', next:'timing'},
      timing: {show:'timing'},
      urgency: {bot:'Do you prefer low-irritation progression? / Bạn ưu tiên lộ trình ít kích ứng?', next:'tolerance'},
      tolerance: {show:'tolerance'},
      close: {bot:'Great. We will prepare your assigned onboarding form. / Tốt. Hệ thống sẽ mở form khởi tạo liệu trình cho bạn.', end:true}
    };
    const c = map[step];
    if(!c) return;
    if(c.bot) setTimeout(()=>addChatBubble(c.bot,'bot'),250);
    if(c.show) document.querySelector(`[data-chat-options="${c.show}"]`)?.classList.remove('hidden');
    if(c.end) document.querySelector('[data-chat-form]')?.classList.remove('hidden');
  }

  function initChat(){
    if(!document.querySelector('[data-chat-log]')) return;
    runChatStep('start');
  }

  applyState(body.dataset.state || 'pre-diagnosis');
  initQuiz();
  initChat();
})();
