function copyFunc() {
            var copyBtn = document.getElementById("copyBtn");
            navigator.clipboard.writeText(window.location.href).then(() => {
                copyBtn.textContent = "Link Copied!"
                copyBtn.style.backgroundColor = "#2bb447"
            }).catch(() => {
                alert("ho gya hoga!");
            });

        }

function pls_wait(){
  document.getElementById("please_wait_container_id").classList.add("show");
}
function closeBlur(event) {
    main = document.getElementById("main_content_id")
    document.getElementById("please_wait_container_id").style.display = "none";
    main.style.filter = "";
    main.style.pointerEvents = "all";
}

function create_auto_suggest_item(item, moviedb_img_path){
      let temp_node = document.querySelector("#auto_suggest_item_temp").content.cloneNode(true);
      poster = item["poster_path"];
      posterUrl = moviedb_img_path + poster;
      temp_node.querySelector("img").src = posterUrl;
      temp_node.querySelector("li").setAttribute("name",item["name"]);
      temp_node.querySelector("img").setAttribute("name",item["name"]);
      temp_node.querySelector("li").innerHTML = `${item["name"]} - ${item["first_air_date"]} | ${item["origin_country"][0]}<br><br>${item["overview"].slice(0, 100)}...`;
      return temp_node;
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
