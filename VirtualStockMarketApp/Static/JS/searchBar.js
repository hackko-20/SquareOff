//https://cloud.iexapis.com/stable/stock/MSFT/quote?token=pk_245073c85596466aa6afff012f007125
let api_key = "pk_245073c85596466aa6afff012f007125"
let stock_symbol;
function search_api() {
    let key = document.getElementById('searchbar').value
    key = key.toUpperCase();
    let url = "https://cloud.iexapis.com/" + "stable/stock/" + key + "/quote?token=" + api_key;
    console.log(url);
    fetch(url)
        .then(response => {
            
            if (response.status === 200)
            {
                stock = response.json();
                var element = document.createElement("div");
                element.setAttribute("id","link");
                element.setAttribute("class","stockDetails");
                link.innerHTML=stock["symbol"];
                document.getElementById("searchOption").appendChild(element);
                document.getElementById("stock_symbol").setAttribute("value",stock["symbol"]);
            }  
            else
            {
                alert("Enter valid stock symbol");
            }
        })
        .catch(error => {
            if(error == 404)
                alert('Stock symbol does not match');
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
    console.log("in");
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