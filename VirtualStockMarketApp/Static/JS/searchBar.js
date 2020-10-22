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
        })
        .catch(error =>{
            alert("symbol not found");
            var prevLinks = document.getElementsByClassName("StockLink");
            for(var i=0;i<prevLinks.length;i++)
            {
                prevLinks[i].remove();
            }
            document.getElementById("watermark").style.display = "block";
        });  
}

function openForm(evt, formName) {
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

function switchCL(e, price) {
    console.log("iinnnn");
    var value = e.target.value;
    var field = document.getElementsByClassName("price");
    console.log("in");
    for (var i=0;i<field.length;i++)
    {
        if (value === "current")
        {
            field[i].setAttribute("placeholder", price);
            field[i].readonly = true;
        }
        else
        {
            field[i].setAttribute("placeholder", "");
            field[i].removeAttribute("readonly");
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