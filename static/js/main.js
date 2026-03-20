console.log("main.js loaded");

// ---------------------------------------
// ローディング
// ---------------------------------------

window.addEventListener("load", function () {
  const loading = document.getElementById("loading");
  loading.style.display = "none";
});


// ---------------------------------------
// ユーザ側
// ---------------------------------------

// 商品絞り込み
function filterSeries(series) {
  const products = document.querySelectorAll(".productWrapper");
  products.forEach((p) => {
    if (series === "All" || p.dataset.series === series) {
      p.style.display = "block";
    } else {
      p.style.display = "none";
    }
  });
}
function filterColor(color) {
  const products = document.querySelectorAll(".productWrapper");
  products.forEach((p) => {
    if (p.dataset.color === color) {
      p.style.display = "block";
    } else {
      p.style.display = "none";
    }
  });
}

// 検索ボックス
function toggleInvisible() {
  const searchBox = document.querySelector(".searchBox");
  searchBox.classList.toggle("invisible");
}


// ---------------------------------------
// 管理者側
// ---------------------------------------

// 登録商品画像プレビュー
document.getElementById("img_file").addEventListener("change", function(e){
  const file = e.target.files[0]
  if(file){
    const reader = new FileReader()
    reader.onload = function(event){
      document.getElementById("img_preview").src = event.target.result
      // 表示切替
      document.getElementById("img_preview").style.display="block";
      document.getElementById("current_img").style.display="none";
    }
    reader.readAsDataURL(file)
  }
})

// 注文情報絞り込み
function filterProsessing(processing) {
  const orders = document.querySelectorAll(".adminOrder");
  orders.forEach((o) => {
    if (processing === "All" || o.dataset.processing === String(processing)) {
      o.style.display = "table-row";
    } else {
      o.style.display = "none";
    }
  });
}
