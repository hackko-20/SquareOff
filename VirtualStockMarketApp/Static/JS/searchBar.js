//https://cloud.iexapis.com/stable/stock/MSFT/quote?token=pk_245073c85596466aa6afff012f007125
let api_key = "pk_245073c85596466aa6afff012f007125";
let stock_symbol;
function search_api() {
    let key = document.getElementById('searchbar').value
    key = key.toUpperCase();
    let url = "https://cloud.iexapis.com/" + "stable/stock/" + key + "/quote?token=" + api_key;
    console.log(url);
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
                var element = document.createElement("button");
                element.setAttribute("type","submit");
                element.setAttribute("class","StockLink");
                document.getElementById("ss").value = data.symbol;
                console.log(document.getElementById("ss").value);
                element.innerHTML="See details about the stock" + data.companyName;
                document.getElementById("searchOption").appendChild(element);
                })
        .catch(error =>{
            alert("symbol not found");
        });  
}

function openForm(evt, formName ) {
    var i, formElement, tablinks;
    formElement = document.getElementsByClassName("formElements");
    for (i = 0; i < formElement.length; i++) {
        formElement[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(formName).style.display = "block";
    evt.currentTarget.className += " active";
}

function switchCL() {
    var field = document.getElementById("LimitCheck")[0].value;
    var element = document.createElement("div");
    comsole.log("in");
    if(value === "current")
    {
        element.innerHTML = '<input type="number" name="price" placeholder="current price">';
    }
    else
    {
        element.innerHTML = '<input type="number" name="price" placeholder="limit price">';
    }
    document.getElementById("Intraday").appendChild(element);
}