window.onload = function(){
    document.querySelectorAll("a.pls_wait").forEach( item => {
        item.addEventListener("click", pls_wait)
    });
//    document.querySelector("#main_content_id").addEventListener("click", function(){
//     if(document.querySelector("#main_content_id").style.filter == "blur(10px)"){
//         document.querySelector("#main_content_id").style.filter = "";
//         document.querySelector("#main_content_id").style.pointerEvents = "all";
//     }
//    });
}
function pls_wait(event){
    main = document.getElementById("main_content_id")
    document.getElementById("please_wait_container_id").style.display="flex";
    main.style.filter = "blur(10px)";
    main.style.pointerEvents = "none";
}
function copyFunc() {
    var copyBtn = document.getElementById("copyBtn");
    navigator.clipboard.writeText(copyBtn.value);
    copyBtn.textContent = "Link Copied!"
    copyBtn.style.backgroundColor = "#2bb447"
}

function closeBlur(event){
    main = document.getElementById("main_content_id")
    document.getElementById("please_wait_container_id").style.display="none";
    main.style.filter = "";
    main.style.pointerEvents = "all";
}