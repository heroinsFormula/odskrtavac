const xhttp = new XMLHttpRequest();
function handleChange(checkbox) {

    if (checkbox.checked === true) { // if checked
        alert("checked");    
        xmlhttp.open("POST", "../PHP/test.php");
        xmlhttp.send();
    } else{
        alert("unchecked");
   }
}