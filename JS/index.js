const xhttp = new XMLHttpRequest();
function handleChange(checkbox) {
    // let params = `id=${checkbox.id}`;
    // checkbox.checked ? params += `&checked=true` : params += `&checked=false`;
    // xhttp.open('POST', 'add_to_db.php');
    // xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    // xhttp.send(params);

    $.ajax({
        type: 'POST',
        url: 'add_to_db.php',
        data: jQuery.param({ id: `${checkbox.id}`, checked : `${checkbox.checked}`}) ,
        contentType: 'application/x-www-form-urlencoded',
    });

    let row = checkbox.closest('tr');
    let row_data = row.children;
    let table = checkbox.closest('table');
    let new_row = table.insertRow(-1);

    Array.from(row_data).forEach((data) => {
        let cell = new_row.insertCell(-1);
        cell.innerHTML = data.innerHTML;
        row.remove();

    });

}


function drop_titles() {
    $.ajax({
        url: 'remove_all.php',
        contentType: 'application/x-www-form-urlencoded',
    });
}


function openNav() {
    document.getElementById("myNav").style.width = "50%";
  }


  function closeNav() {
    document.getElementById("myNav").style.width = "0%";
}