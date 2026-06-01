const map = new maplibregl.Map({
  container: "map",

  style: {
    version: 8,
    sources: {
      gsi: {
        type: "raster",
        tiles: [
          "https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg"
        ],
        tileSize: 256,
        attribution: "国土地理院"
      }
    },
    layers: [
      {
        id: "gsi",
        type: "raster",
        source: "gsi"
      }
    ]
  },

  center: [140.1, 35.7],
  zoom: 9
});

map.addControl(new maplibregl.NavigationControl());

const stores = [

  /* =====================
     浦安エリア
  ===================== */
  {
    name: "楽 遊食屋 浦安店",
    lng: 139.892176,
    lat: 35.665692,
    station: "浦安駅",
    walk: "徒歩1分",
    info: "24時間営業・年中無休（居酒屋）",
    url: "https://www.google.com/maps/search/?api=1&query=楽遊食屋浦安店"
  },
  {
    name: "マルヤス酒場 浦安店",
    lng: 139.9017,
    lat: 35.6652,
    station: "浦安駅",
    walk: "徒歩1分",
    info: "24時間営業・年中無休（居酒屋）",
    url: "https://www.google.com/maps/search/?api=1&query=マルヤス酒場浦安店"
  },

  /* =====================
     船橋エリア
  ===================== */
  {
    name: "マルヤス酒場 船橋店",
    lng: 139.9854,
    lat: 35.7008,
    station: "京成船橋駅",
    walk: "徒歩1分",
    info: "24時間営業・年中無休（居酒屋）",
    url: "https://www.google.com/maps/search/?api=1&query=マルヤス酒場船橋店"
  },
  {
    name: "酔っ手羽 船橋店",
    lng: 139.9851,
    lat: 35.7010,
    station: "船橋駅",
    walk: "徒歩3分",
    info: "24時間営業・年中無休（大衆居酒屋）",
    url: "https://www.google.com/maps/search/?api=1&query=酔っ手羽船橋店"
  },

  /* =====================
     柏エリア
  ===================== */
  {
    name: "マルヤス酒場 柏店",
    lng: 139.9705,
    lat: 35.8620,
    station: "柏駅",
    walk: "徒歩1分",
    info: "24時間営業・年中無休（居酒屋）",
    url: "https://www.google.com/maps/search/?api=1&query=マルヤス酒場柏店"
  },

  /* =====================
     千葉・中心エリア
  ===================== */
  {
    name: "磯丸水産 千葉駅前店",
    lng: 140.1149,
    lat: 35.6116,
    station: "千葉駅",
    walk: "徒歩3分",
    info: "24時間営業・年中無休（海鮮居酒屋）",
    url: "https://www.google.com/maps/search/?api=1&query=磯丸水産千葉駅前店"
  },
  {
    name: "磯丸水産 千葉中央駅前店",
    lng: 140.1227,
    lat: 35.6074,
    station: "千葉中央駅",
    walk: "徒歩1分",
    info: "24時間営業・年中無休（海鮮居酒屋）",
    url: "https://www.google.com/maps/search/?api=1&query=磯丸水産千葉中央駅前店"
  },
  {
    name: "磯丸水産 西船橋店",
    lng: 139.9807,
    lat: 35.7074,
    station: "西船橋駅",
    walk: "徒歩2分",
    info: "24時間営業・年中無休（海鮮居酒屋）",
    url: "https://www.google.com/maps/search/?api=1&query=磯丸水産西船橋店"
  },
  {
    name: "磯丸水産 松戸西口駅前店",
    lng: 139.9008,
    lat: 35.7846,
    station: "松戸駅",
    walk: "徒歩1分",
    info: "24時間営業・年中無休（海鮮居酒屋）",
    url: "https://www.google.com/maps/search/?api=1&query=磯丸水産松戸西口駅前店"
  }

];

stores.forEach(s => {

  const popup = new maplibregl.Popup().setHTML(`
    <h3>${s.name}</h3>
    <p>${s.info}</p>
    <p>最寄駅：${s.station}</p>
    <p>${s.walk}</p>
    <a href="${s.url}" target="_blank">Googleマップでルート</a>
  `);

  new maplibregl.Marker({ color: "red" })
    .setLngLat([s.lng, s.lat])
    .setPopup(popup)
    .addTo(map);

});   