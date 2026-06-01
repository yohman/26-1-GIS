// ===== 地図 =====

const map = new maplibregl.Map({

    container: 'map',

    style: 'https://demotiles.maplibre.org/style.json',

    center: [139.767, 35.681],

    zoom: 1.5,

});

// ===== 場所データ =====

const locations = [

    {
        lng: 24.138056,
        lat: -71.526111,
        name: "旧カルデア",
        image: "ノウムカルデア.jpeg"
    },

    {
        lng: 2.3522,
        lat: 48.8566,
        name: "１部１章",
        image: "１部１章.jpeg"
    },

    {
        lng: 12.4964,
        lat: 41.9028,
        name: "１部２章",
        image: "１部２章.jpeg"
    },

    {
        lng: -160.0,
        lat: 0.0,
        name: "１部３章",
        image: "１部３章.jpeg"
    },

    {
        lng: -0.1276,
        lat: 51.5072,
        name: "１部４章",
        image: "１部４章.jpeg"
    },

    {
        lng: -100.0,
        lat: 45.0,
        name: "１部５章",
        image: "１部５章.jpeg"
    },

    {
        lng: 35.2137,
        lat: 31.7683,
        name: "１部６章",
        image: "１部６章.jpeg"
    },

    {
        lng: 47.8150,
        lat: 30.5085,
        name: "１部７章",
        image: "１部７章.jpeg"
    }
];

// ===== 修復管理 =====

let humanityBurned = false;

const repairedSingularities = [];

// ===== 終章データ =====

const finalChapter = {

    lng: 0,
    lat: 85,
    name: "終章 ソロモン",
    image: "１部終章.jpeg"

};

let finalChapterUnlocked = false;

// ===== 地球儀 =====

map.on('style.load', () => {

    map.setProjection({
        type: 'globe'
    });

    // ===== ズームボタン =====

    map.addControl(
        new maplibregl.NavigationControl()
    );

    // ===== 赤い地球レイヤー =====

    map.addLayer({

        id: 'burn-layer',

        type: 'background',

        paint: {
            'background-color': '#8B0000'
        }

    });

    // 最初は非表示

    map.setLayoutProperty(
        'burn-layer',
        'visibility',
        'none'
    );

    // ===== マーカー =====

    locations.forEach(loc => {

        const popup = new maplibregl.Popup({
            offset: 25
        })

        .setHTML(`

            <h2>${loc.name}</h2>

            <img
                src="${loc.image}"
                width="250"
                style="
                    border-radius: 10px;
                    margin-top: 10px;
                "
            >

            <br>

            <button
                class="repair-button"
                onclick="repairHumanity('${loc.name}')"
            >
                人理修復
            </button>

        `);

        new maplibregl.Marker({
            color: "red"
        })

        .setLngLat([loc.lng, loc.lat])

        .setPopup(popup)

        .addTo(map);

    });

});

// ===== 人理修復 =====

function repairHumanity(placeName){

    // 人理焼却前は無効

    if(!humanityBurned){

        alert("先に人理焼却を開始してください");

        return;

    }

    // 重複防止

    if(repairedSingularities.includes(placeName)){

        alert(placeName + " は既に修復済みです");

        return;

    }

    // 修復記録

    repairedSingularities.push(placeName);

    alert(placeName + " の人理修復をしました！");

    // 必要数チェック

    if(
        repairedSingularities.length === locations.length
        &&
        !finalChapterUnlocked
    ){

        unlockFinalChapter();

    }

}

// ===== 地図移動 =====

function moveToPlace(lng, lat){

    map.flyTo({

        center: [lng, lat],

        zoom: 5,

        speed: 0.8

    });

}

// ===== 人理焼却 =====

function burnHumanity(){

    humanityBurned = true;

    // 赤い背景を表示

    map.setLayoutProperty(
        'burn-layer',
        'visibility',
        'visible'
    );

    alert("人理焼却が開始されました");

}

// ===== 終章解放 =====

function unlockFinalChapter(){

    finalChapterUnlocked = true;

    alert("冠位時間神殿ソロモンが出現しました");

    // ポップアップ

    const popup = new maplibregl.Popup({
        offset: 25
    })

    .setHTML(`

        <h2>${finalChapter.name}</h2>

        <img
            src="${finalChapter.image}"
            width="250"
            style="
                border-radius: 10px;
                margin-top: 10px;
            "
        >

        <br>

        <button
            class="repair-button"
            onclick="showFinalBattle()"
        >
            最終決戦
        </button>

    `);

    // マーカー生成

    new maplibregl.Marker({
        color: "purple"
    })

    .setLngLat([
        finalChapter.lng,
        finalChapter.lat
    ])

    .setPopup(popup)

    .addTo(map);

    // 左メニューに追加

    const menu = document.getElementById("menu");

    const button = document.createElement("button");

    button.className = "place-button";

    button.innerText = "１部終章";

    button.onclick = () => {

        moveToPlace(
            finalChapter.lng,
            finalChapter.lat
        );

    };

    menu.appendChild(button);

}

// ===== 最終決戦 =====

function showFinalBattle(){

    // 既に表示済みなら作らない

    if(document.getElementById("final-battle-screen")){

        return;

    }

    // ===== 画面 =====

    const battleScreen = document.createElement("div");

    battleScreen.id = "final-battle-screen";

    battleScreen.style.position = "fixed";

    battleScreen.style.top = "0";

    battleScreen.style.left = "0";

    battleScreen.style.width = "100vw";

    battleScreen.style.height = "100vh";

    battleScreen.style.backgroundColor = "black";

    battleScreen.style.display = "flex";

    battleScreen.style.justifyContent = "center";

    battleScreen.style.alignItems = "center";

    battleScreen.style.zIndex = "9999";

    // ===== 画像 =====

    const image = document.createElement("img");

    image.src = "１部ゲーティア戦.jpeg";

    image.style.maxWidth = "90%";

    image.style.maxHeight = "90%";

    image.style.borderRadius = "10px";

    image.id = "battle-image";

    // ===== 説明 =====

    const text = document.createElement("div");

    text.innerText = "クリックで次へ";

    text.style.position = "absolute";

    text.style.bottom = "30px";

    text.style.color = "white";

    text.style.fontSize = "20px";

    // ===== 追加 =====

    battleScreen.appendChild(image);

    battleScreen.appendChild(text);

    document.body.appendChild(battleScreen);

    // ===== 次の画像へ =====

    battleScreen.onclick = () => {

        showSecondBattleImage();

    };

}

// ===== 2枚目 =====

function showSecondBattleImage(){

    const screen = document.getElementById(
        "final-battle-screen"
    );

    screen.innerHTML = "";

    // ===== 画像 =====

    const image = document.createElement("img");

    image.src = "ゲーティア最終決戦.jpeg";

    image.style.maxWidth = "90%";

    image.style.maxHeight = "90%";

    image.style.borderRadius = "10px";

    image.style.position = "relative";

    // ===== 透明クリック判定 =====

    const ringArea = document.createElement("div");

    ringArea.style.position = "absolute";

    /*
        ↓ 指輪の位置に合わせて調整
    */

    ringArea.style.bottom = "220px";

    ringArea.style.right = "110px";

    /*
        ↓ 判定サイズ
    */

    ringArea.style.width = "120px";

    ringArea.style.height = "120px";

    /*
        ↓ デバッグ用
        完成後は transparent にする
    */

    ringArea.style.backgroundColor =
        "rgba(255,0,0,0.3)";

    ringArea.style.cursor = "pointer";

    ringArea.style.zIndex = "10000";

    // ===== クリック =====

    ringArea.onclick = (event) => {

        event.stopPropagation();

        playFinalVideo();

    };

    // ===== 追加 =====

    screen.appendChild(image);
    screen.appendChild(ringArea);
    screen.appendChild(text);
}

// ===== 最終動画再生 =====

function playFinalVideo(){

    // ===== 画面取得 =====

    const screen = document.getElementById(
        "final-battle-screen"
    );

    // ===== 中身を消す =====

    screen.innerHTML = "";

    // ===== 動画 =====

    const video = document.createElement("video");

    video.src = "１部最終演出.mp4";

    video.autoplay = true;

    video.controls = false;

    video.style.width = "100vw";

    video.style.height = "100vh";

    video.style.objectFit = "cover";

    // ===== 追加 =====

    screen.appendChild(video);

    // ===== 動画終了 =====

    video.onended = () => {

        showEnding();

    };

}

// ===== エンディング =====

function showEnding(){

    // ===== 最終画面取得 =====

    const screen = document.getElementById(
        "final-battle-screen"
    );

    // ===== 地図色を元に戻す =====

    map.setLayoutProperty(
        'burn-layer',
        'visibility',
        'none'
    );

    // ===== 左メニュー非表示 =====

    const menu = document.getElementById("menu");

    menu.style.display = "none";

    // ===== 人理焼却ボタン非表示 =====

    const burnButton = document.getElementById(
        "burn-button"
    );

    burnButton.style.display = "none";

    // ===== MapLibreマーカー非表示 =====

    const markers = document.querySelectorAll(
        ".maplibregl-marker"
    );

    markers.forEach(marker => {

        marker.style.display = "none";

    });

    // ===== ポップアップ非表示 =====

    const popups = document.querySelectorAll(
        ".maplibregl-popup"
    );

    popups.forEach(popup => {

        popup.style.display = "none";

    });

    // ===== 画面変更 =====

    screen.innerHTML = "";

    screen.style.backgroundColor = "black";

    // ===== メッセージ =====

    const message = document.createElement("div");

    message.innerText =
        "おめでとう。君のおかげで人理焼却は防がれた";

    message.style.color = "white";

    message.style.fontSize = "40px";

    message.style.textAlign = "center";

    message.style.padding = "30px";

    // ===== 表示 =====

    screen.appendChild(message);

}
