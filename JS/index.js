const xhttp = new XMLHttpRequest();
function handleChange(checkbox) {
    let params = `id=${checkbox.id}`;
    checkbox.checked ? params += `&checked=true` : params += `&checked=false`;
    xhttp.open('POST', 'add_to_db.php');
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.send(params);


    let row = checkbox.closest('tr');
    let row_data = row.children;
    let table_read = document.getElementById('Přečteno');
    let new_row = table_read.insertRow(-1);

    Array.from(row_data).forEach((data) => {
        let cell = new_row.insertCell(-1);
        cell.innerHTML = data.innerHTML;
        row.style.display = 'none';
    });

}