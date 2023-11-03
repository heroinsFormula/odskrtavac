const xhttp = new XMLHttpRequest();
function handleChange(checkbox) {
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        // if (checkbox.checked === true) { 
            
        // } else{

        // }
        }
    };
    console.log(checkbox.checked);
    if (checkbox.checked === true) {
        var params = `id=${checkbox.id}&checked=true`;
    } else if (checkbox.checked === false) {
        var params = `id=${checkbox.id}&checked=false`;
    }    
    xhttp.open("POST", "add_to_db.php");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhttp.send(params);
}