window.onload = function() {
    document.querySelectorAll(".pls_wait").forEach(item => {
        item.addEventListener("click", pls_wait)
    });
}

function pls_wait(event) {
    main = document.getElementById("main_content_id")
    document.getElementById("please_wait_container_id").style.display = "flex";
    main.style.filter = "blur(10px)";
    main.style.pointerEvents = "none";
}

function copyFunc() {
    var copyBtn = document.getElementById("copyBtn");
    navigator.clipboard.writeText(copyBtn.value).then(() => {
        copyBtn.textContent = "Link Copied!"
        copyBtn.style.backgroundColor = "#2bb447"
    }).catch(() => {
        alert("pata ni");
    });

}

function closeBlur(event) {
    main = document.getElementById("main_content_id")
    document.getElementById("please_wait_container_id").style.display = "none";
    main.style.filter = "";
    main.style.pointerEvents = "all";
}