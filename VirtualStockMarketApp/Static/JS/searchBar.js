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
                var prevLinks = document.getElementsByClassName("StockLink");
                for(var i=0;i<prevLinks.length;i++)
                {
                    prevLinks[i].remove();
                }
                element.setAttribute("type", "submit");
                element.setAttribute("class", "StockLink");
                document.getElementById("ss").value = data.symbol;
                console.log(document.getElementById("ss").value);
                element.innerHTML= data.companyName;
                document.getElementById("searchOption").appendChild(element);
                document.getElementById("watermark").style.display = "none";
                document.getElementById("addToFav").value = key;
                document.getElementById("FavButton").disabled = false;
        })
        .catch(error => {
            alert("symbol not found");
            var prevLinks = document.getElementsByClassName("StockLink");
            for(var i=0;i<prevLinks.length;i++)
            {
                prevLinks[i].remove();
            }
            document.getElementById("watermark").style.display = "block";
            document.getElementById("FavButton").disabled = true;
        });  
}

function openForm(evt, formName, price) {
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
    var selectFields = document.querySelectorAll(".LimitCheck option")
    for( i = 0; i < selectFields.length; i++)
    {
        selectFields[i].selected = selectFields[i].defaultSelected;
    }

    //the price input
    var priceField = document.getElementsByClassName("price")
    for( i = 0; i < priceField.length; i++)
    {
        priceField[i].value = price;
        priceField[i].readOnly = true;
    }
}

function switchCL(e, price) {
    var value = e.target.value;
    var field = document.getElementsByClassName("price");
    for (var i=0;i<field.length;i++)
    {
        if (value === "current")
        {
            field[i].value = price;
            field[i].readOnly = true;
        }
        else
        {
            field[i].removeAttribute("readonly");
            field[i].readOnly = false;
        }       
    }
    
}

function myFunction() {
    var x = document.getElementById("myLinks");
    if (x.style.display === "block") {
      x.style.display = "none";
    } else {
      x.style.display = "block";
    }
}

function myFunction2() {
    var x = document.getElementById("myLinks2");
    if (x.style.display === "block") {
      x.style.display = "none";
    } else {
      x.style.display = "block";
    }
}