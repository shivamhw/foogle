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
        alert("ho gya hoga!");
    });

}

function closeBlur(event) {
    main = document.getElementById("main_content_id")
    document.getElementById("please_wait_container_id").style.display = "none";
    main.style.filter = "";
    main.style.pointerEvents = "all";
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
        // console.log(curr_val); 
        //   LIMIT = "1GB";
        if(curr_val[curr_val.length-2] == " "){ 
            continue;
        }
        if(curr_val[curr_val.length-2] != LIMIT[LIMIT.length-2]){
          if(LIMIT[LIMIT.length-2] == "G"){
            // console.log("Allowing "+curr_val)
            rs[i].style.display = "";
          }else{
            rs[i].style.display = "none";
            // console.log("rejecting "+curr_val);
          }
        }else{
          curr_val_flt = parseFloat(curr_val.slice(0, curr_val.indexOf(" ")))
        //   console.log(curr_val_flt);
        //   console.log(LIMIT.slice(0, LIMIT.indexOf(" ")))
        //   console.log(LIMIT.slice(0, LIMIT.indexOf(" ")) > curr_val_flt)
          if(LIMIT.slice(0, LIMIT.indexOf(" ")) > curr_val_flt){
            //   allow
            // console.log("Allow B")
            rs[i].style.display = "";
          }else{
            // console.log("Rejtc B");
            //   diasallow
          rs[i].style.display = "none";
          }
        }
      }
}