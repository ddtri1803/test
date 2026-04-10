(function () {
  function sendEvent(type, payload) {
    fetch('/api/tracking-event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: type, payload: payload || {}, ts: Date.now() })
    }).catch(function () {});
  }

  window.V11Pixel = {
    view: function (slug) { sendEvent('view', { slug: slug }); },
    click: function (slug, cta) { sendEvent('click', { slug: slug, cta: cta }); },
    purchase: function (slug, value) { sendEvent('purchase', { slug: slug, value: value }); }
  };
})();
