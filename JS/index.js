const xhttp = new XMLHttpRequest();
function handleChange(checkbox) {
    let params = `id=${checkbox.id}`;
    checkbox.checked ? params += `&checked=true` : params += `&checked=false`;
    xhttp.open('POST', 'add_to_db.php');
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.send(params);
}