console.log("main.js loaded");

function filterSeries(series) {

    console.log("test");

    const products = document.querySelectorAll('.productWrapper');

    products.forEach(p => {
        if (series === 'All' || p.dataset.series === series) {
            p.style.display = "block";
        } else {
            p.style.display = "none";
        }
    });
}

function filterColor(color) {

    console.log("test2");

    const products = document.querySelectorAll('.productWrapper');

    products.forEach(p => {
        if (p.dataset.color === color) {
            p.style.display = "block";
        } else {
            p.style.display = "none";
        }
    });
}

function toggleInvisible() {

    console.log("test3");

    const searchBox = document.querySelector('.searchBox');

    searchBox.classList.toggle('invisible');
}

// ローディング
window.addEventListener("load", function() {
    const loading = document.getElementById("loading");
    loading.style.display = "none";
});

