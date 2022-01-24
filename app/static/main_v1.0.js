window.onload = function () {
    document.querySelectorAll(".pls_wait").forEach(item => {
        item.addEventListener("click", pls_wait)
    });

    const searchForm = document.querySelector(".search_box");
    const input = document.querySelector("input");
    let child = document.querySelector(".auto-box");
    input.addEventListener("keyup", async () => {
        let box = document.getElementById("auto_box_id");
        if (input.value.length == 0){
            box.style.display = "none";
            document.getElementById("suggest_box_id").style.display="block";
            return;
        }
        document.getElementById("suggest_box_id").style.display="none";

        box.style.display = "block";
        url = `https://api.themoviedb.org/3/search/movie?api_key=31833e5be915a6e5621728ce631edac1&language=en-US&query=${input.value}&page=1&include_adult=false`
        res = await (await fetch(url)).json();
        child.innerHTML = "";
        res["results"].forEach(item => {
            child.innerHTML += `<li><a href="/search?search_box=${item["title"]} ${item["release_date"].slice(0, 4)}">${item["title"]} - ${item["release_date"]}</a></li>`
        });
    });

    async function up (){
        const sugg = document.querySelector(".suggest");
        url = "https://api.themoviedb.org/3/movie/popular?api_key=31833e5be915a6e5621728ce631edac1&language=en-IN&page=1";
        let res = await (await fetch(url)).json();
        sugg.innerHTML ="Trending <br>";
        res["results"].forEach( item => {
                sugg.innerHTML += `<li><a href="/search?search_box=${item["title"]} ${item["release_date"].slice(0, 4)}">${item["title"]}</a></li>`
            });
        }
        up();
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