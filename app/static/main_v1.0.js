window.onload = function () {
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
            navigator.clipboard.writeText(window.location.href).then(() => {
                copyBtn.textContent = "Link Copied!"
                copyBtn.style.backgroundColor = "#2bb447"
            }).catch(() => {
                alert("ho gya hoga!");
            });

        }

function closeBlur(event) {
    main = document.getElementById("main_content_id")
    document.getElementById("please_wait_container_id").style.display = "none";
    main.style.filter = "";
    main.style.pointerEvents = "all";
}

function ListItemCopy(e) {
  toggleSuggest(0);
  document.querySelector("input").value = e.target.getAttribute("name");
  return;
}

function toggleSuggest(flg){
  if(flg == 0 ){
  document.getElementById("search_box_div_id").classList.remove("expand");
  document.getElementById("auto_box_id").classList.remove("shown");
  }else{
    document.getElementById("search_box_div_id").classList.add("expand")
    document.getElementById("auto_box_id").classList.add("shown")
  }
}

function filterBySize(event){
    LIMIT = String(event.value)
    rs = document.querySelectorAll("tr")
    if(LIMIT == "INF"){
        for(let i=1;i<rs.length;i++){
            rs[i].style.display = "";
            
        }
        return;
    }
    console.log(LIMIT);
    for(let i=1;i<rs.length;i++){
        curr_val = String(rs[i].children[1].innerText);
        if(curr_val[curr_val.length-2] == " "){ 
            continue;
        }
        if(curr_val[curr_val.length-2] != LIMIT[LIMIT.length-2]){
          if(LIMIT[LIMIT.length-2] == "G"){
            rs[i].style.display = "";
          }else{
            rs[i].style.display = "none";
          }
        }else{
          curr_val_flt = parseFloat(curr_val.slice(0, curr_val.indexOf(" ")))
          if(LIMIT.slice(0, LIMIT.indexOf(" ")) > curr_val_flt){
            rs[i].style.display = "";
          }else{
          rs[i].style.display = "none";
          }
        }
      }
}
