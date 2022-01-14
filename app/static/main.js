function copyFunc() {
    var copyBtn = document.getElementById("copyBtn");
    navigator.clipboard.writeText(copyBtn.value);
    copyBtn.textContent = "Link Copied!"
    copyBtn.style.backgroundColor = "#2bb447"
}