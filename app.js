const PRODUCT_FILE = 'danh_muc_san_pham_da_lieu.csv';
const REGIMEN_FILE = 'bo_san_pham_lieu_trinh_da_lieu.csv';

// Ảnh thực tế về sản phẩm skincare/dermatology (nguồn ảnh công khai từ Unsplash)
const productImages = {
  'DL-SRM-001': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?auto=format&fit=crop&w=1000&q=80',
  'DL-TON-002': 'https://images.unsplash.com/photo-1629198688000-71f23e745b6e?auto=format&fit=crop&w=1000&q=80',
  'DL-SER-003': 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?auto=format&fit=crop&w=1000&q=80',
  'DL-SER-004': 'https://images.unsplash.com/photo-1607602132700-06825845be6c?auto=format&fit=crop&w=1000&q=80',
  'DL-CRM-005': 'https://images.unsplash.com/photo-1625772452859-1c03d5bf1137?auto=format&fit=crop&w=1000&q=80',
  'DL-SS-006': 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?auto=format&fit=crop&w=1000&q=80',
  'DL-ACN-007': 'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?auto=format&fit=crop&w=1000&q=80',
  'DL-RET-008': 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=1000&q=80'
};

const fallbackImage = 'https://images.unsplash.com/photo-1556228720-da6dad2d5f1a?auto=format&fit=crop&w=1000&q=80';

function parseCSV(filePath) {
  return new Promise((resolve, reject) => {
    Papa.parse(filePath, {
      download: true,
      header: true,
      skipEmptyLines: true,
      complete: (results) => resolve(results.data),
      error: (error) => reject(error)
    });
  });
}

function renderProducts(products) {
  const grid = document.getElementById('productsGrid');
  grid.innerHTML = '';

  products.forEach((p) => {
    const image = productImages[p['Mã sản phẩm']] || fallbackImage;
    const item = document.createElement('article');
    item.className = 'bg-slate-50 border border-slate-200 rounded-xl overflow-hidden';
    item.innerHTML = `
      <img src="${image}" alt="Hình ảnh sản phẩm ${p['Tên sản phẩm']}" class="w-full h-48 object-cover" loading="lazy" />
      <div class="p-4 space-y-2 text-sm">
        <div class="flex items-center justify-between gap-2">
          <span class="inline-block px-2 py-1 rounded bg-slate-200 text-slate-800 text-xs font-semibold">${p['Mã sản phẩm']}</span>
          <span class="text-xs text-slate-600">${p['Quy cách']}</span>
        </div>
        <h3 class="font-semibold text-base text-slate-900">${p['Tên sản phẩm']}</h3>
        <p><b>Loại da:</b> ${p['Loại da phù hợp']}</p>
        <p><b>Công dụng:</b> ${p['Công dụng chính']}</p>
        <p><b>Thành phần:</b> ${p['Thành phần nổi bật']}</p>
        <p><b>Cách dùng:</b> ${p['Cách dùng']}</p>
        <p class="text-slate-700"><b>Giới thiệu:</b> ${p['Giới thiệu sản phẩm']}</p>
        <p class="font-semibold text-emerald-700">Giá tham khảo: ${Number(p['Giá tham khảo (VNĐ)']).toLocaleString('vi-VN')} VNĐ</p>
      </div>
    `;
    grid.appendChild(item);
  });

  document.getElementById('productStats').textContent = `Đang hiển thị ${products.length} sản phẩm.`;
}

function renderRegimens(regimens, productsByCode) {
  const wrap = document.getElementById('regimenList');
  wrap.innerHTML = '';

  regimens.forEach((r) => {
    const codes = (r['Danh sách sản phẩm (mã)'] || '')
      .split(';')
      .map((x) => x.trim())
      .filter(Boolean);

    const chips = codes
      .map((code) => {
        const name = productsByCode[code]?.['Tên sản phẩm'] || 'Chưa có dữ liệu';
        return `<li class="bg-white border border-slate-200 rounded px-2 py-1"><span class="font-semibold">${code}</span> — ${name}</li>`;
      })
      .join('');

    const card = document.createElement('article');
    card.className = 'border border-slate-200 rounded-xl p-4 bg-slate-50';
    card.innerHTML = `
      <div class="flex flex-wrap items-center gap-2 mb-2">
        <span class="bg-indigo-600 text-white px-2 py-1 rounded text-xs font-semibold">${r['Mã bộ']}</span>
        <h3 class="font-semibold text-slate-900">${r['Tên bộ sản phẩm']}</h3>
      </div>
      <p class="text-sm mb-1"><b>Mục tiêu:</b> ${r['Mục tiêu liệu trình']}</p>
      <p class="text-sm mb-1"><b>Loại da phù hợp:</b> ${r['Loại da phù hợp']}</p>
      <p class="text-sm mb-1"><b>Thời gian gợi ý:</b> ${r['Thời gian gợi ý']}</p>
      <p class="text-sm mb-2"><b>Hướng dẫn dùng:</b> ${r['Hướng dẫn sử dụng theo thứ tự']}</p>
      <p class="text-sm mb-2"><b>Kỳ vọng:</b> ${r['Kỳ vọng cải thiện']}</p>
      <ul class="text-sm grid md:grid-cols-2 gap-2">${chips}</ul>
    `;
    wrap.appendChild(card);
  });
}

function attachSearch(allProducts) {
  const input = document.getElementById('productSearch');
  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    if (!q) {
      renderProducts(allProducts);
      return;
    }

    const filtered = allProducts.filter((p) =>
      Object.values(p).some((v) => String(v).toLowerCase().includes(q))
    );

    renderProducts(filtered);
  });
}

async function start() {
  try {
    const [products, regimens] = await Promise.all([
      parseCSV(PRODUCT_FILE),
      parseCSV(REGIMEN_FILE)
    ]);

    const productsByCode = Object.fromEntries(products.map((p) => [p['Mã sản phẩm'], p]));

    renderProducts(products);
    renderRegimens(regimens, productsByCode);
    attachSearch(products);
  } catch (error) {
    document.body.innerHTML = `<div class="max-w-3xl mx-auto p-6"><h1 class="text-xl font-bold mb-2">Không thể đọc dữ liệu CSV</h1><p>Vui lòng chạy web bằng server local (ví dụ: <code>python -m http.server 8000</code>) rồi truy cập <code>http://localhost:8000</code>.</p><pre class="mt-4 bg-slate-100 p-3 rounded text-xs">${String(error)}</pre></div>`;
  }
}

start();
