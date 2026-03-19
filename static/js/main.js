console.log("main.js loaded");

// ユーザ側の商品絞り込み

function filterSeries(series) {
  console.log("test");

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
  console.log("test2");

  const products = document.querySelectorAll(".productWrapper");

  products.forEach((p) => {
    if (p.dataset.color === color) {
      p.style.display = "block";
    } else {
      p.style.display = "none";
    }
  });
}

function toggleInvisible() {
  console.log("test3");

  const searchBox = document.querySelector(".searchBox");

  searchBox.classList.toggle("invisible");
}


// ローディング

window.addEventListener("load", function () {
  const loading = document.getElementById("loading");
  loading.style.display = "none";
});


// 管理者側の登録商品画像プレビュー

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
