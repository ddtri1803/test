const PRODUCT_FILE = 'danh_muc_san_pham_da_lieu.csv';
const REGIMEN_FILE = 'bo_san_pham_lieu_trinh_da_lieu.csv';

function createLocalImage(code, name) {
  const safeName = (name || '').replace(/[<&>]/g, '');
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='800' height='500'>
    <defs><linearGradient id='g' x1='0' x2='1' y1='0' y2='1'><stop offset='0%' stop-color='#1d4ed8'/><stop offset='100%' stop-color='#0ea5e9'/></linearGradient></defs>
    <rect width='100%' height='100%' fill='url(#g)'/>
    <text x='50%' y='42%' dominant-baseline='middle' text-anchor='middle' font-size='36' fill='white' font-family='Arial' font-weight='bold'>${code}</text>
    <text x='50%' y='56%' dominant-baseline='middle' text-anchor='middle' font-size='24' fill='white' font-family='Arial'>${safeName}</text>
    <text x='50%' y='74%' dominant-baseline='middle' text-anchor='middle' font-size='16' fill='#dbeafe' font-family='Arial'>Hình minh họa sản phẩm</text>
  </svg>`;
  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
}

function splitCSVLine(line) {
  const values = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"';
        i += 1;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === ',' && !inQuotes) {
      values.push(current);
      current = '';
    } else {
      current += ch;
    }
  }

  values.push(current);
  return values.map((v) => v.trim());
}

function parseCSVText(csvText) {
  const lines = csvText
    .replace(/^\uFEFF/, '')
    .split(/\r?\n/)
    .filter((line) => line.trim().length > 0);

  if (lines.length < 2) {
    return [];
  }

  const headers = splitCSVLine(lines[0]);
  return lines.slice(1).map((line) => {
    const values = splitCSVLine(line);
    const row = {};
    headers.forEach((header, index) => {
      row[header] = values[index] ?? '';
    });
    return row;
  });
}

async function parseCSV(filePath) {
  const response = await fetch(filePath);
  if (!response.ok) {
    throw new Error(`Không tìm thấy file: ${filePath} (HTTP ${response.status})`);
  }
  const csvText = await response.text();
  return parseCSVText(csvText);
}

function renderProducts(products) {
  const grid = document.getElementById('productsGrid');
  grid.innerHTML = '';

  products.forEach((p) => {
    const image = createLocalImage(p['Mã sản phẩm'], p['Tên sản phẩm']);
    const item = document.createElement('article');
    item.className = 'bg-slate-50 border border-slate-200 rounded-xl overflow-hidden';
    item.innerHTML = `
      <img src="${image}" alt="Hình sản phẩm ${p['Tên sản phẩm']}" class="w-full h-48 object-cover" loading="lazy" />
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
        <p class="font-semibold text-emerald-700">Giá tham khảo: ${Number(p['Giá tham khảo (VNĐ)'] || 0).toLocaleString('vi-VN')} VNĐ</p>
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
    document.body.innerHTML = `<div class="max-w-3xl mx-auto p-6"><h1 class="text-xl font-bold mb-2">Không thể tải dữ liệu</h1><p class="mb-2">Lỗi chính: ${String(error)}</p><p>Hãy đảm bảo 2 file CSV cùng thư mục với <code>index.html</code>, rồi chạy bằng server local: <code>python -m http.server 8000</code>.</p></div>`;
  }
}

start();
