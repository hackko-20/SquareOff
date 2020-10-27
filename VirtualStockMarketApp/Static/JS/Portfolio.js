function openForm(evt, divisionName ) {
    var i, divisionElement, tablinks;
    divisionElement = document.getElementsByClassName("commonElements");
    for (i = 0; i < divisionElement.length; i++) {
        divisionElement[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(divisionName).style.display = "block";
    evt.currentTarget.className += " active";
}

function openDiv( divisionName ) {
    var i, divisionElement;
    divisionElement = document.getElementsByClassName("subClass");
    for (i = 0; i < divisionElement.length; i++) {
        divisionElement[i].style.display = "none";
    }
    document.getElementById(divisionName).style.display = "block";
}