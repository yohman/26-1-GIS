// main.js - MapLibre による地図表示とマーカー管理
(function(){
  console.log('Script loaded');
  const center = [139.977, 35.862]; // 初期中心座標（経度, 緯度）
  const mapContainer = document.getElementById('map');
  if(!mapContainer){
    console.error('Map container not found');
    return;
  }
  console.log('Creating map...');
  const map = new maplibregl.Map({
    container: 'map',
    style: { version: 8, sources: {}, layers: [] },
    center: center,
    zoom: 12,
    pitch: 45,
    bearing: 0,
    antialias: true
  });
  console.log('Map created');

  const shops = [];
  const DEFAULT_SHOPS = [
  { name: "すみれ", lat: 43.0687, lon: 141.3545, prefecture: "北海道", address: "北海道札幌市", hours: "", photo: "", url: "" },
  { name: "長尾中華そば", lat: 40.8244, lon: 140.74, prefecture: "青森県", address: "青森県青森市", hours: "", photo: "", url: "" },
  { name: "柳家", lat: 39.7036, lon: 141.1527, prefecture: "岩手県", address: "岩手県盛岡市", hours: "", photo: "", url: "" },
  { name: "麺屋とがし", lat: 38.2682, lon: 140.8719, prefecture: "宮城県", address: "宮城県仙台市", hours: "", photo: "", url: "" },
  { name: "末廣ラーメン本舗", lat: 39.7199, lon: 140.1024, prefecture: "秋田県", address: "秋田県秋田市", hours: "", photo: "", url: "" },
  { name: "龍上海", lat: 38.2554, lon: 140.3633, prefecture: "山形県", address: "山形県山辺町", hours: "", photo: "", url: "" },
  { name: "坂内食堂", lat: 37.65, lon: 139.993, prefecture: "福島県", address: "福島県喜多方市", hours: "", photo: "", url: "" },
  { name: "活龍", lat: 36.0824, lon: 140.0836, prefecture: "茨城県", address: "茨城県土浦市", hours: "", photo: "", url: "" },
  { name: "佐野らーめん万里", lat: 36.3147, lon: 139.5836, prefecture: "栃木県", address: "栃木県佐野市", hours: "", photo: "", url: "" },
  { name: "だるま大使", lat: 36.3222, lon: 139.0094, prefecture: "群馬県", address: "群馬県高崎市", hours: "", photo: "", url: "" },
  { name: "狼煙", lat: 35.8617, lon: 139.6233, prefecture: "埼玉県", address: "埼玉県さいたま市", hours: "", photo: "", url: "" },
  { name: "中華蕎麦 とみ田", lat: 35.7835, lon: 139.9006, prefecture: "千葉県", address: "千葉県北松戸市", hours: "", photo: "", url: "" },
  { name: "麺屋一燈", lat: 35.7448, lon: 139.7196, prefecture: "東京都", address: "東京都新宿区", hours: "", photo: "", url: "" },
  { name: "吉村家", lat: 35.4662, lon: 139.638, prefecture: "神奈川県", address: "神奈川県横浜市", hours: "", photo: "", url: "" },
  { name: "青島食堂", lat: 37.4464, lon: 138.7681, prefecture: "新潟県", address: "新潟県新潟市", hours: "", photo: "", url: "" },
  { name: "麺家いろは", lat: 36.6953, lon: 137.2113, prefecture: "富山県", address: "富山県富山市", hours: "", photo: "", url: "" },
  { name: "神仙", lat: 36.5613, lon: 136.6562, prefecture: "石川県", address: "石川県金沢市", hours: "", photo: "", url: "" },
  { name: "一力", lat: 35.6452, lon: 136.2206, prefecture: "福井県", address: "福井県敦賀市", hours: "", photo: "", url: "" },
  { name: "蓬来軒", lat: 35.6639, lon: 138.5683, prefecture: "山梨県", address: "山梨県甲府市", hours: "", photo: "", url: "" },
  { name: "気むずかし家", lat: 36.6485, lon: 138.181, prefecture: "長野県", address: "長野県松本市", hours: "", photo: "", url: "" },
  { name: "麺屋しらかわ", lat: 36.1461, lon: 137.2522, prefecture: "岐阜県", address: "岐阜県高山市", hours: "", photo: "", url: "" },
  { name: "麺屋燕", lat: 34.8361, lon: 138.1894, prefecture: "静岡県", address: "静岡県静岡市", hours: "", photo: "", url: "" },
  { name: "如水", lat: 35.1815, lon: 136.9066, prefecture: "愛知県", address: "愛知県名古屋市", hours: "", photo: "", url: "" },
  { name: "鉢ノ葦葉", lat: 34.965, lon: 136.6256, prefecture: "三重県", address: "三重県津市", hours: "", photo: "", url: "" },
  { name: "ラーメンにっこう", lat: 35.2745, lon: 136.2597, prefecture: "滋賀県", address: "滋賀県大津市", hours: "", photo: "", url: "" },
  { name: "新福菜館", lat: 35.0037, lon: 135.7681, prefecture: "京都府", address: "京都府京都市", hours: "", photo: "", url: "" },
  { name: "人類みな麺類", lat: 34.733, lon: 135.5, prefecture: "大阪府", address: "大阪府大阪市", hours: "", photo: "", url: "" },
  { name: "もっこす", lat: 34.6901, lon: 135.1955, prefecture: "兵庫県", address: "兵庫県神戸市", hours: "", photo: "", url: "" },
  { name: "まりお流", lat: 34.6851, lon: 135.8048, prefecture: "奈良県", address: "奈良県奈良市", hours: "", photo: "", url: "" },
  { name: "井出商店", lat: 34.2305, lon: 135.1675, prefecture: "和歌山県", address: "和歌山県和歌山市", hours: "", photo: "", url: "" },
  { name: "香味徳", lat: 35.5038, lon: 133.825, prefecture: "鳥取県", address: "鳥取県鳥取市", hours: "", photo: "", url: "" },
  { name: "神楽", lat: 35.4723, lon: 133.05, prefecture: "島根県", address: "島根県松江市", hours: "", photo: "", url: "" },
  { name: "天神そば", lat: 34.6618, lon: 133.9344, prefecture: "岡山県", address: "岡山県岡山市", hours: "", photo: "", url: "" },
  { name: "陽気", lat: 34.3853, lon: 132.4553, prefecture: "広島県", address: "広島県広島市", hours: "", photo: "", url: "" },
  { name: "一久", lat: 33.9516, lon: 131.2517, prefecture: "山口県", address: "山口県宇部市", hours: "", photo: "", url: "" },
  { name: "いのたに", lat: 34.0703, lon: 134.5548, prefecture: "徳島県", address: "徳島県徳島市", hours: "", photo: "", url: "" },
  { name: "はまんど", lat: 34.1828, lon: 133.7075, prefecture: "香川県", address: "香川県高松市", hours: "", photo: "", url: "" },
  { name: "瓢太", lat: 33.8392, lon: 132.7657, prefecture: "愛媛県", address: "愛媛県松山市", hours: "", photo: "", url: "" },
  { name: "自由軒", lat: 33.5597, lon: 133.5311, prefecture: "高知県", address: "高知県高知市", hours: "", photo: "", url: "" },
  { name: "一蘭 本社総本店", lat: 33.5887, lon: 130.3997, prefecture: "福岡県", address: "福岡県福岡市", hours: "", photo: "", url: "" },
  { name: "幸陽閣", lat: 33.2635, lon: 130.3008, prefecture: "佐賀県", address: "佐賀県佐賀市", hours: "", photo: "", url: "" },
  { name: "思案橋ラーメン", lat: 32.7448, lon: 129.8787, prefecture: "長崎県", address: "長崎県長崎市", hours: "", photo: "", url: "" },
  { name: "黒亭", lat: 32.8031, lon: 130.7071, prefecture: "熊本県", address: "熊本県熊本市", hours: "", photo: "", url: "" },
  { name: "ふくやラーメン", lat: 33.2396, lon: 131.6126, prefecture: "大分県", address: "大分県大分市", hours: "", photo: "", url: "" },
  { name: "ラーメンマン", lat: 31.9111, lon: 131.4239, prefecture: "宮崎県", address: "宮崎県宮崎市", hours: "", photo: "", url: "" },
  { name: "こむらさき", lat: 31.5966, lon: 130.5576, prefecture: "鹿児島県", address: "鹿児島県鹿児島市", hours: "", photo: "", url: "" },
  { name: "通堂", lat: 26.2124, lon: 127.6811, prefecture: "沖縄県", address: "沖縄県那覇市", hours: "", photo: "", url: "" },
  { name: "ラーメン二郎 三田本店", lat: 35.6477, lon: 139.7495, prefecture: "東京都", address: "東京都港区", hours: "", photo: "", url: "" },
  { name: "飯田商店", lat: 35.1448, lon: 139.106, prefecture: "神奈川県", address: "神奈川県横浜市", hours: "", photo: "", url: "" },
  { name: "六厘舎", lat: 35.6812, lon: 139.7718, prefecture: "東京都", address: "東京都千代田区", hours: "", photo: "", url: "" },
  { name: "春木屋 荻窪本店", lat: 35.704, lon: 139.62, prefecture: "東京都", address: "東京都杉並区", hours: "", photo: "", url: "" },
  { name: "支那そばや 本店", lat: 35.4662, lon: 139.638, prefecture: "神奈川県", address: "神奈川県横浜市", hours: "", photo: "", url: "" },
  { name: "琴平荘", lat: 38.727, lon: 139.995, prefecture: "山形県", address: "山形県山辺町", hours: "", photo: "", url: "" },
  { name: "天下一品 総本店", lat: 35.03, lon: 135.779, prefecture: "京都府", address: "京都府京都市", hours: "", photo: "", url: "" },
  { name: "一風堂 大名本店", lat: 33.5887, lon: 130.3968, prefecture: "福岡県", address: "福岡県福岡市", hours: "", photo: "", url: "" },
  { name: "ラーメン山岡家 柏店", lat: 35.8685, lon: 140.149, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" },
  { name: "8番らーめん", lat: 36.5613, lon: 136.6562, prefecture: "石川県", address: "石川県金沢市", hours: "", photo: "", url: "" },
  { name: "王道家", lat: 35.8485, lon: 139.9727, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" },
  { name: "誉", lat: 35.862, lon: 139.9715, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" },
  { name: "宗八", lat: 35.861, lon: 139.972, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" },
  { name: "めん吉", lat: 35.844, lon: 139.955, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" },
  { name: "AKEBI", lat: 35.8615, lon: 139.973, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" },
  { name: "ramen ibuto", lat: 35.8608, lon: 139.9735, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" },
  { name: "麺屋こうじ", lat: 35.858, lon: 139.971, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" },
  { name: "テラチョウ", lat: 35.8575, lon: 139.9705, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" },
  { name: "ひむろ", lat: 35.857, lon: 139.968, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" },
  { name: "一蘭 柏店", lat: 35.85, lon: 139.98, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" },
  { name: "丸源ラーメン 柏店", lat: 35.852, lon: 139.9805, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" },
  { name: "幸楽苑 柏豊町店", lat: 35.86, lon: 139.962, prefecture: "千葉県", address: "千葉県柏市", hours: "", photo: "", url: "" }
  ];
  let shopMarkers = [];
  let remoteMarkers = [];
  const GOOGLE_PLACES_API_KEY = '';

  // ユーティリティ: テキスト正規化（比較用）
  function normalizeText(s){
    if(!s) return '';
    return String(s).toLowerCase().replace(/[^\w\u3040-\u30ff\u4e00-\u9fff]+/g,'').trim();
  }

  function generateIndexTabs(){
    const tabsContainer = document.getElementById('index-tabs');
    if(!tabsContainer) return;
    tabsContainer.innerHTML = '';
    
    // 全店舗から最初の文字を抽出してユニークにしてソート
    const firstChars = new Set(shopMarkers.map(m => (m.item.name || '')[0])).values();
    const sortedChars = Array.from(firstChars).sort();
    
    const allBtn = document.createElement('button');
    allBtn.textContent = 'すべて';
    allBtn.className = 'active';
    allBtn.addEventListener('click', ()=>{
      document.getElementById('search').value = '';
      document.querySelectorAll('#index-tabs button').forEach(b=>b.classList.remove('active'));
      allBtn.classList.add('active');
      populateList();
      document.getElementById('search-status').textContent = '';
    });
    tabsContainer.appendChild(allBtn);
    
    sortedChars.forEach(char=>{
      const btn = document.createElement('button');
      btn.textContent = char;
      btn.addEventListener('click', ()=>{
        document.getElementById('search').value = '';
        document.querySelectorAll('#index-tabs button').forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');
        const filtered = shopMarkers.filter(m => (m.item.name || '')[0] === char);
        populateList(filtered);
        document.getElementById('search-status').textContent = `${filtered.length} 件`;
      });
      tabsContainer.appendChild(btn);
    });
  }

  function avgRating(item){
    if(!item.reviews || item.reviews.length===0) return null;
    const s = item.reviews.reduce((a,b)=>a+b.score,0);
    return (s / item.reviews.length);
  }

  // より厳密な重複判定: 名前一致かつ住所一致、または近接かつ名前一致
  function isDuplicateItem(newItem){
    const normalized = normalizeItem(newItem);
    if(!normalized || !normalized.name) return false;
    const nName = normalizeText(normalized.name);
    const nAddr = normalizeText(normalized.address || '');
    for(const m of shopMarkers){
      const it = m.item;
      const iname = normalizeText(it.name);
      const iaddr = normalizeText(it.address || '');
      if(iname && nName && iname === nName){
        if(iaddr && nAddr && iaddr === nAddr) return true;
        if(it.lat != null && it.lon != null && normalized.lat != null && normalized.lon != null){
          const d = haversine(it.lat, it.lon, normalized.lat, normalized.lon);
          if(d < 0.2) return true;
        } else {
          return true;
        }
      }
    }
    return false;
  }

  function popupHtml(item){
    return `
      <div class="popup">
        ${item.photo?`<img src="${item.photo}" alt="${item.name}">`:''}
        <strong>${item.name}</strong>
        <div>${item.address || ''}</div>
        <div>${item.hours || ''}</div>
        ${item.url?`<div><a href="${item.url}" target="_blank">公式サイト</a></div>`:''}
      </div>`;
  }

  function normalizeItem(item){
    if(!item || typeof item !== 'object') return null;
    const normalized = {};
    for(const key of Object.keys(item)){
      normalized[key.trim().toLowerCase()] = item[key];
    }
    const result = {
      name: normalized.name || normalized.shop || normalized.title || '',
      address: normalized.address || normalized.addr || normalized['addr:full'] || normalized['addr:street'] || normalized['addr:city'] || '',
      hours: normalized.hours || normalized.opening_hours || normalized.open || '',
      photo: normalized.photo || normalized.image || normalized.img || '',
      url: normalized.url || normalized.website || '',
      city: normalized.city || '',
      prefecture: normalized.prefecture || normalized.state || normalized.region || normalized['県'] || '',
      _remote: normalized._remote || false,
      reviews: Array.isArray(normalized.reviews) ? normalized.reviews : [],
    };
    const lat = normalized.lat || normalized.latitude || normalized['緯度'];
    const lon = normalized.lon || normalized.longitude || normalized.lng || normalized.lngt || normalized['経度'];
    result.lat = lat != null && lat !== '' ? Number(lat) : null;
    result.lon = lon != null && lon !== '' ? Number(lon) : null;
    return result;
  }

  function addMarker(item){
    if(!item) return;
    const normalized = normalizeItem(item);
    if(!normalized.name) return;
    if(!normalized.reviews) normalized.reviews = [];
    let marker = null;
    if(normalized.lat != null && normalized.lon != null && !Number.isNaN(normalized.lat) && !Number.isNaN(normalized.lon)){
      const el = document.createElement('div');
      el.className = 'marker' + (normalized._remote? ' remote':'' );
      marker = new maplibregl.Marker(el)
        .setLngLat([normalized.lon, normalized.lat])
        .setPopup(new maplibregl.Popup({offset:12}).setHTML(popupHtml(normalized)))
        .addTo(map);
    }
    shopMarkers.push({marker, item: normalized});
    if(normalized._remote && marker) remoteMarkers.push({marker, item: normalized});
    if(!shops.includes(normalized)) shops.push(normalized);
  }

  function clearRemoteMarkers(){
    remoteMarkers.forEach(m=>{ try{ m.marker.remove(); }catch(e){} });
    remoteMarkers = [];
    // also remove from shopMarkers
    shopMarkers = shopMarkers.filter(m=>!m.item._remote);
  }

  function populateList(filteredMarkers=null){
    const ul = document.getElementById('shop-list');
    ul.innerHTML = '';
    const list = filteredMarkers || shopMarkers;
    const query = document.getElementById('search').value || '';
    if(list.length === 0){
      const li = document.createElement('li');
      li.textContent = '該当する店舗はありません。';
      li.style.color = '#666';
      ul.appendChild(li);
      return;
    }
    // ソート設定を尊重して表示
    const sort = document.getElementById('sort') ? document.getElementById('sort').value : 'relevance';
    const center = map.getCenter();
    const enriched = list.map(m=>{
      const distance = m.item.lat && m.item.lon ? haversine(center.lat, center.lng, m.item.lat, m.item.lon) : null;
      const rating = avgRating(m.item);
      return {m, distance, rating};
    });
    if(sort === 'distance') enriched.sort((a,b)=> (a.distance||9999) - (b.distance||9999));
    else if(sort === 'rating') enriched.sort((a,b)=> (b.rating||0) - (a.rating||0));
    // relevance は既存順（データ追加順）
    enriched.forEach(e=>{
      const m = e.m;
      const li = document.createElement('li');
      const meta = [];
      if(e.distance!=null) meta.push(`${e.distance.toFixed(2)} km`);
      else meta.push('位置情報なし');
      if(e.rating!=null) meta.push(`評価 ${e.rating.toFixed(1)}`);
      const highlightedName = highlightSearchTerm(m.item.name, query);
      const prefecture = m.item.prefecture ? `【${m.item.prefecture}】` : '';
      const address = m.item.address ? `<div style="font-size:11px;color:#999;margin-top:2px">${m.item.address}</div>` : '';
      li.innerHTML = `<div class="name">${highlightedName} ${prefecture}</div>${address}<div class="meta" style="font-size:12px;color:#666">${meta.join(' ・ ')}</div>`;
      li.addEventListener('click', ()=>{
        flyToShop(m);
        showDetail(m.item);
      });
      ul.appendChild(li);
    });
    generateIndexTabs();
    renderListView();
  }

  function flyToShop(entry){
    if(!entry || !entry.marker || !entry.item) return;
    map.flyTo({center:[entry.item.lon, entry.item.lat], zoom:15});
    entry.marker.togglePopup();
  }

  function getListViewItems(query, sortBy){
    const q = normalizeText(query || '');
    let list = shopMarkers.slice();
    if(q){
      list = list.filter(m => {
        const name = normalizeText(m.item.name || '');
        const address = normalizeText(m.item.address || '');
        const city = normalizeText(m.item.city || '');
        const prefecture = normalizeText(m.item.prefecture || '');
        return name.includes(q) || address.includes(q) || city.includes(q) || prefecture.includes(q);
      });
    }
    if(sortBy === 'name'){
      list.sort((a,b)=>(a.item.name||'').localeCompare(b.item.name||'', 'ja'));
    } else if(sortBy === 'prefecture'){
      list.sort((a,b)=>{
        const r = (a.item.prefecture||'').localeCompare(b.item.prefecture||'', 'ja');
        return r || (a.item.name||'').localeCompare(b.item.name||'', 'ja');
      });
    }
    return list;
  }

  function renderListView(){
    const view = document.getElementById('shop-list-view');
    if(!view) return;
    const query = document.getElementById('list-search') ? document.getElementById('list-search').value : '';
    const sortBy = document.getElementById('list-sort') ? document.getElementById('list-sort').value : 'order';
    const items = getListViewItems(query, sortBy);
    const countLabel = document.getElementById('list-count');
    if(countLabel) countLabel.textContent = `計 ${items.length} 件`;
    if(items.length === 0){
      view.innerHTML = '<div style="padding:16px;color:#666">該当する店舗はありません。</div>';
      return;
    }

    const rows = items.map((m, index)=>{
      const item = m.item;
      const prefecture = item.prefecture ? `<span class="prefecture">${item.prefecture}</span>` : '';
      return `
        <tr data-index="${index}">
          <td class="rank">${index + 1}</td>
          <td class="name">${escapeHtml(item.name)}</td>
          <td>${prefecture}</td>
          <td class="address">${escapeHtml(item.address || '')}</td>
          <td class="coords">${item.lat != null && item.lon != null ? `${item.lat.toFixed(4)}, ${item.lon.toFixed(4)}` : ''}</td>
        </tr>`;
    }).join('');

    view.innerHTML = `
      <table class="shop-list-table">
        <thead>
          <tr>
            <th class="rank">No</th>
            <th>店舗名</th>
            <th>都道府県</th>
            <th>住所</th>
            <th>座標</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>`;

    view.querySelectorAll('tbody tr').forEach((tr, idx)=>{
      tr.addEventListener('click', ()=>{
        const markerEntry = items[idx];
        flyToShop(markerEntry);
        const mapTabButton = document.querySelector('.main-tab-btn[data-tab="map"]');
        if(mapTabButton) mapTabButton.click();
      });
    });
  }

  function activateMainTabs(){
    const buttons = document.querySelectorAll('.main-tab-btn');
    const contents = document.querySelectorAll('.main-tab-content');
    buttons.forEach(btn => btn.addEventListener('click', ()=>{
      buttons.forEach(b=>b.classList.toggle('active', b===btn));
      contents.forEach(c=> c.classList.toggle('active', c.dataset.tab === btn.dataset.tab));
      if(btn.dataset.tab === 'list'){
        renderListView();
      }
    }));
  }

  function escapeRegExp(value){
    return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function escapeHtml(text){
    if(!text) return '';
    return String(text).replace(/[&<>"]+/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[ch] || ch);
  }

  function highlightSearchTerm(text, query){
    if(!query) return text;
    const escaped = escapeRegExp(query);
    const regex = new RegExp(`(${escaped})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }

  function getFilteredMarkers(query){
    if(!query) return shopMarkers;
    const q = normalizeText(query);
    return shopMarkers.filter(m => {
      const name = normalizeText(m.item.name || '');
      const address = normalizeText(m.item.address || '');
      const city = normalizeText(m.item.city || '');
      const prefecture = normalizeText(m.item.prefecture || '');
      return name.includes(q) || address.includes(q) || city.includes(q) || prefecture.includes(q);
    });
  }

  // Overpass API を使った全国検索 (日本のbboxで制限)
  async function overpassSearch(name){
    const q = name.replace(/[-/\\^$*+?.()|[\]{}]/g,'\\$&'); // エスケープ
    const bbox = '20,122,46,154'; // south,west,north,east (日本全域)
    const body = `[out:json][timeout:25];(node["name"~"${q}",i](${bbox});way["name"~"${q}",i](${bbox});relation["name"~"${q}",i](${bbox}););out center;`;
    const url = 'https://overpass-api.de/api/interpreter';
    try{
      const res = await fetch(url, { method:'POST', body });
      if(!res.ok) throw new Error('Overpass error ' + res.status);
      const data = await res.json();
      const items = data.elements.map(el=>{
        const lat = el.type === 'node' ? el.lat : (el.center && el.center.lat);
        const lon = el.type === 'node' ? el.lon : (el.center && el.center.lon);
        return {
          name: el.tags && (el.tags.name || el.tags['name:ja'] || ''),
          lat: lat,
          lon: lon,
          address: [el.tags && el.tags['addr:full'], el.tags && el.tags['addr:street'], el.tags && el.tags['addr:city']].filter(Boolean).join(' '),
          hours: el.tags && (el.tags.opening_hours || ''),
          photo: null,
          url: el.tags && el.tags.website,
          _remote: true,
        };
      }).filter(it=>it.lat && it.lon && it.name);
      return items;
    }catch(err){
      console.warn('Overpass search failed', err);
      throw err;
    }
  }

  async function googlePlacesSearch(name){
    if(!GOOGLE_PLACES_API_KEY) throw new Error('Google API key is not configured.');
    const query = `${name} ラーメン`;
    const url = `https://maps.googleapis.com/maps/api/place/textsearch/json?query=${encodeURIComponent(query)}&language=ja&region=jp&key=${encodeURIComponent(GOOGLE_PLACES_API_KEY)}`;
    const res = await fetch(url);
    if(!res.ok) throw new Error('Google Places error ' + res.status);
    const data = await res.json();
    if(data.status !== 'OK' && data.status !== 'ZERO_RESULTS'){
      throw new Error('Google Places failed: ' + data.status);
    }
    const items = (data.results || []).map(result=>({
      name: result.name,
      lat: result.geometry?.location?.lat,
      lon: result.geometry?.location?.lng,
      address: result.formatted_address || '',
      hours: '',
      photo: result.photos && result.photos[0] ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=320&photoreference=${result.photos[0].photo_reference}&key=${encodeURIComponent(GOOGLE_PLACES_API_KEY)}` : null,
      url: result.place_id ? `https://www.google.com/maps/place/?q=place_id:${result.place_id}` : '',
      _remote: true,
    })).filter(it=>it.lat && it.lon && it.name);
    return items;
  }

  function loadSampleData(){
    console.log('Loading sample data...');
    return fetch('data/ramen.json')
      .then(r=>{
        console.log('Fetch response status:', r.status);
        if(!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(data=>{
        if(!Array.isArray(data)) throw new Error('Invalid sample data');
        console.log('Sample data loaded:', data.length, 'items');
        data.forEach(d=>{
          if(!shops.includes(d)) shops.push(d);
          addMarker(d);
        });
        populateList();
      })
      .catch(err=>{
        console.warn('サンプルデータ読み込み失敗:', err);
        loadLocalDataset(DEFAULT_SHOPS);
      });
  }

  async function reverseGeocode(lat, lon){
    const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lon)}&accept-language=ja&addressdetails=1`;
    try{
      const res = await fetch(url, { headers: { 'User-Agent': 'ra-men-map/1.0 (+https://example.com)' } });
      if(!res.ok) throw new Error('Reverse geocode failed');
      const data = await res.json();
      return data.address || {};
    }catch(err){
      console.warn('reverseGeocode error', err);
      return null;
    }
  }

  function formatRegionLabel(address){
    if(!address) return '';
    const prefecture = address.state || address['県'] || address.region || '';
    const city = address.city || address.town || address.village || address.county || '';
    return [prefecture, city].filter(Boolean).join(' ');
  }

  function updateRegionText(text){
    const label = document.getElementById('region-label');
    if(!label) return;
    label.textContent = text || '位置情報を表示';
  }

  function setBaseMapStyle(style){
    const osmVisible = style === 'osm' ? 'visible' : 'none';
    const satVisible = style === 'satellite' ? 'visible' : 'none';
    if(map.getLayer('osm-layer')) map.setLayoutProperty('osm-layer', 'visibility', osmVisible);
    if(map.getLayer('satellite-layer')) map.setLayoutProperty('satellite-layer', 'visibility', satVisible);
  }

  function haversine(lat1, lon1, lat2, lon2){
    const toRad = deg => deg * Math.PI / 180;
    const R = 6371; // km
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a = Math.sin(dLat/2) * Math.sin(dLat/2)
      + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2))
      * Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  }

  function scheduleRegionUpdate(){
    const center = map.getCenter();
    const key = `${center.lat.toFixed(4)},${center.lng.toFixed(4)},${map.getZoom().toFixed(2)}`;
    if(key === lastRegionKey) return;
    lastRegionKey = key;
    if(regionTimeout) clearTimeout(regionTimeout);
    regionTimeout = setTimeout(async ()=>{
      const address = await reverseGeocode(center.lat, center.lng);
      updateRegionText(formatRegionLabel(address));
    }, 250);
  }

  let regionTimeout = null;
  let lastRegionKey = '';

  map.on('load', ()=>{
    // OpenStreetMap のラスタタイルをベースマップとして追加
    // 軽いデモ用途向けです。大量利用の際は利用規約にご注意ください。
    map.addSource('osm', {
      type: 'raster',
      tiles: [
        'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
      ],
      tileSize: 256
    });
    map.addLayer({
      id: 'osm-layer',
      type: 'raster',
      source: 'osm',
      paint: { 'raster-opacity': 1 }
    });

    map.addSource('satellite', {
      type: 'raster',
      tiles: [
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
      ],
      tileSize: 256
    });
    map.addLayer({
      id: 'satellite-layer',
      type: 'raster',
      source: 'satellite',
      paint: { 'raster-opacity': 1 }
    });

    setBaseMapStyle('osm');

    const mapStyleSelect = document.getElementById('map-style');
    if(mapStyleSelect){
      mapStyleSelect.addEventListener('change', (ev)=>{
        setBaseMapStyle(ev.target.value);
      });
    }

    // サンプルデータ読み込み
    loadSampleData();

    scheduleRegionUpdate();
  });

  map.on('moveend', scheduleRegionUpdate);
  map.on('zoomend', scheduleRegionUpdate);

  // 検索入力による絞り込み
  const searchInput = document.getElementById('search');
  document.getElementById('nationwide').checked = false;
  document.getElementById('google-search').checked = false;
  let searchTimeout = null;
  searchInput.addEventListener('input', (ev)=>{
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(async ()=>{
      const q = ev.target.value || '';
      // 検索入力時：索引タブをリセット
      document.querySelectorAll('#index-tabs button').forEach(b=>b.classList.remove('active'));
      const allBtn = document.querySelector('#index-tabs button:first-child');
      if(allBtn) allBtn.classList.add('active');
      
      const nationwide = document.getElementById('nationwide').checked;
      const googleSearch = document.getElementById('google-search').checked;
      const status = document.getElementById('search-status');
      const tasks = [];
      if((nationwide || googleSearch) && q.trim().length>1){
        status.textContent = '全国検索中...';
        clearRemoteMarkers();
        if(nationwide){
          tasks.push(overpassSearch(q).then(items=>({source:'overpass', items})).catch(err=>{ return {source:'overpass', error:err}; }));
        }
        if(googleSearch){
          tasks.push(googlePlacesSearch(q).then(items=>({source:'google', items})).catch(err=>({source:'google', error:err})));
        }
        const results = await Promise.all(tasks);
        let added = 0;
        let total = 0;
        let errors = [];
        for(const result of results){
          if(result.error){
            errors.push(`${result.source} ${result.error.message}`);
            continue;
          }
          total += result.items.length;
          result.items.forEach(it=>{
            if(!isDuplicateItem(it)){
              it.reviews = [];
              addMarker(it);
              added++;
            }
          });
        }
        populateList(getFilteredMarkers(q));
        if(errors.length>0){
          status.textContent = `取得 ${total} 件、追加 ${added} 件。${errors.join(' / ')}`;
        }else{
          status.textContent = `取得 ${total} 件、追加 ${added} 件`;
        }
      }else{
        const results = getFilteredMarkers(q);
        populateList(results);
        document.getElementById('search-status').textContent = q ? `検索結果 ${results.length} 件` : '';
      }
    }, 150);
  });
  // Enter で先頭の結果に移動
  searchInput.addEventListener('keydown', (ev)=>{
    if(ev.key === 'Enter'){
      ev.preventDefault();
      const q = ev.target.value || '';
      const filtered = getFilteredMarkers(q);
      if(filtered.length>0){
        const m = filtered[0];
        map.flyTo({center:[m.item.lon, m.item.lat], zoom:15});
        m.marker.togglePopup();
      }
    }
  });

  activateMainTabs();
  const listSearch = document.getElementById('list-search');
  if(listSearch) listSearch.addEventListener('input', renderListView);
  const listSort = document.getElementById('list-sort');
  if(listSort) listSort.addEventListener('change', renderListView);

  // 並び替えの変更を監視
  const sortSelect = document.getElementById('sort');
  if(sortSelect) sortSelect.addEventListener('change', ()=>{
    const q = document.getElementById('search').value || '';
    populateList(getFilteredMarkers(q));
  });

  // CSV 出力
  function exportCSV(){
    const q = document.getElementById('search').value || '';
    const rows = getFilteredMarkers(q);
    const center = map.getCenter();
    const lines = [];
    const header = ['name','lat','lon','address','hours','url','rating','distance_km'];
    lines.push(header.join(','));
    rows.forEach(r=>{
      const it = r.item;
      const rating = avgRating(it);
      const dist = it.lat && it.lon ? haversine(center.lat, center.lng, it.lat, it.lon).toFixed(3) : '';
      const vals = [it.name, it.lat, it.lon, it.address||'', it.hours||'', it.url||'', rating!=null?rating.toFixed(2):'', dist];
      // escape double quotes
      const csvLine = vals.map(v=> typeof v === 'string' && v.includes(',') ? '"'+v.replace(/"/g,'""')+'"' : v).join(',');
      lines.push(csvLine);
    });
    const blob = new Blob([lines.join('\n')], {type:'text/csv;charset=utf-8;'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ramen_shops.csv';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }
  const exportBtn = document.getElementById('export-csv');
  if(exportBtn) exportBtn.addEventListener('click', exportCSV);

  const loadDataBtn = document.getElementById('load-data');
  const dataFileInput = document.getElementById('data-file');

  function clearLocalData(){
    shopMarkers.forEach(m=>{ try{ m.marker.remove(); }catch(e){} });
    shopMarkers = [];
    remoteMarkers = [];
    shops.length = 0;
  }

  function parseCSV(text){
    const lines = text.replace(/\r/g,'').split('\n').filter(line=>line.trim());
    if(lines.length === 0) return [];
    const parseRow = (row) => {
      const values = [];
      let current = '';
      let inQuotes = false;
      for(let i = 0; i < row.length; i++){
        const ch = row[i];
        if(inQuotes){
          if(ch === '"'){
            if(row[i+1] === '"'){
              current += '"';
              i++;
            } else {
              inQuotes = false;
            }
          } else {
            current += ch;
          }
        } else {
          if(ch === '"'){
            inQuotes = true;
          } else if(ch === ','){
            values.push(current);
            current = '';
          } else {
            current += ch;
          }
        }
      }
      values.push(current);
      return values;
    };
    const headers = parseRow(lines[0]).map(h=>h.trim().toLowerCase());
    return lines.slice(1).map(line=>{
      const cols = parseRow(line);
      const item = {};
      headers.forEach((key, idx)=>{ item[key] = cols[idx] !== undefined ? cols[idx].trim() : ''; });
      return item;
    });
  }

  function loadLocalDataset(items){
    if(!Array.isArray(items)) return;
    clearLocalData();
    items.forEach(item=>{
      if(item && item.lat != null && item.lon != null && item.name){
        if(!item.reviews) item.reviews = [];
        addMarker(item);
      }
    });
    populateList();
    document.getElementById('search-status').textContent = `${shopMarkers.length} 件のローカルデータを読み込みました。`;
  }

  if(loadDataBtn && dataFileInput){
    loadDataBtn.addEventListener('click', ()=> dataFileInput.click());
    dataFileInput.addEventListener('change', async (ev)=>{
      const file = ev.target.files && ev.target.files[0];
      if(!file) return;
      try{
        const text = await file.text();
        if(file.name.toLowerCase().endsWith('.csv') || file.type === 'text/csv'){
          const parsed = parseCSV(text);
          if(parsed.length>0){
            loadLocalDataset(parsed);
          }else{
            alert('CSV の解析に失敗しました。フォーマットを確認してください。');
          }
        } else {
          const parsed = JSON.parse(text);
          if(Array.isArray(parsed)){
            loadLocalDataset(parsed);
          }else if(parsed && Array.isArray(parsed.data)){
            loadLocalDataset(parsed.data);
          }else{
            alert('JSON の形式が不正です。配列形式で店舗データを指定してください。');
          }
        }
      }catch(err){
        console.error('Local dataset load failed', err);
        alert('ファイルの読み込みに失敗しました。形式を確認してください。');
      } finally {
        ev.target.value = '';
      }
    });
  }

  // 検索結果を保存
  function saveResults(){
    const q = document.getElementById('search').value || '';
    const rows = getFilteredMarkers(q);
    const data = {
      query: q,
      timestamp: new Date().toISOString(),
      results: rows.map(r=>({
        name: r.item.name,
        lat: r.item.lat,
        lon: r.item.lon,
        address: r.item.address,
        hours: r.item.hours,
        url: r.item.url,
        rating: avgRating(r.item),
        reviews: r.item.reviews || []
      }))
    };
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], {type:'application/json;charset=utf-8;'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ramen_results_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    alert(`${rows.length}件の検索結果を保存しました。`);
  }
  const saveBtn = document.getElementById('save-results');
  if(saveBtn) saveBtn.addEventListener('click', saveResults);
  function showDetail(item){
    // overlay
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.tabIndex = -1;
    const modal = document.createElement('div');
    modal.className = 'modal';
    const rating = avgRating(item);
    modal.innerHTML = `
      <button class="btn-close">閉じる</button>
      <h3>${item.name}</h3>
      ${item.photo?`<img src="${item.photo}" style="max-width:100%;height:auto;margin-bottom:8px">`:''}
      <div>${item.address||''}</div>
      <div>${item.hours||''}</div>
      ${item.url?`<div><a href="${item.url}" target="_blank">公式サイト</a></div>`:''}
      <div style="margin-top:8px">評価: ${rating!=null?rating.toFixed(1):'未評価'}</div>
      <h4>レビュー</h4>
      <ul class="review-list"></ul>
      <form id="review-form">
        <label>点数: <select id="review-score"><option>5</option><option>4</option><option>3</option><option>2</option><option>1</option></select></label>
        <div><textarea id="review-comment" placeholder="感想（任意）」 style="width:100%;height:60px;margin-top:6px"></textarea></div>
        <div style="margin-top:8px"><button type="submit">レビュー投稿</button></div>
      </form>
    `;
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    // render reviews
    function renderReviews(){
      const ul = modal.querySelector('.review-list');
      ul.innerHTML = '';
      if(!item.reviews || item.reviews.length===0){
        const li = document.createElement('li'); li.textContent = 'まだレビューはありません。'; ul.appendChild(li); return;
      }
      item.reviews.slice().reverse().forEach(r=>{
        const li = document.createElement('li');
        li.innerHTML = `<strong>評価 ${r.score}</strong> <div style="font-size:12px;color:#666">${new Date(r.date).toLocaleString()}</div><div>${r.comment||''}</div>`;
        ul.appendChild(li);
      });
    }
    renderReviews();
    // close
    modal.querySelector('.btn-close').addEventListener('click', ()=>{ overlay.remove(); });
    overlay.addEventListener('click', (ev)=>{ if(ev.target === overlay) overlay.remove(); });
    // review submit
    modal.querySelector('#review-form').addEventListener('submit', (ev)=>{
      ev.preventDefault();
      const score = parseInt(modal.querySelector('#review-score').value,10);
      const comment = modal.querySelector('#review-comment').value.trim();
      if(!item.reviews) item.reviews = [];
      item.reviews.push({score, comment, date: Date.now()});
      renderReviews();
      // update popup and list
      for(const m of shopMarkers){ if(m.item === item){ m.marker.setPopup(new maplibregl.Popup({offset:12}).setHTML(popupHtml(item))); break; } }
      populateList(getFilteredMarkers(document.getElementById('search').value || ''));
    });
  }
})();
