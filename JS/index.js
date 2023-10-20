
// on checked - append user_id, book_id to prectene_tituly
// on unchecked - pop read_id
const xhttp = new XMLHttpRequest();
function handleChange(checkbox) {
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        if (checkbox.checked === true) { 
            alert(checkbox.id);    
        } else{
            alert(checkbox.id);
        }
        }
    };
    xhttp.open("GET", "add_to_db.php?id="+checkbox.id);
    xhttp.send();
}