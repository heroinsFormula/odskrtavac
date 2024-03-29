let categories = {
    earlier_1800 : document.getElementById('earlier_1800'),
    earlier_1900 : document.getElementById('earlier_1900'),
    world : document.getElementById('world'),
    czech : document.getElementById('czech'),
    'total' : document.getElementById('total'),
}
let lit_types = {
    prose : document.getElementById('prose'),
    poetry : document.getElementById('poetry'),
    drama : document.getElementById('drama'),
}

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

    

    let row = checkbox.closest('tr'),
        row_data = row.children, 
        read_books = document.getElementById('read_books'),
        not_read = document.getElementById('not_read');

    switch (checkbox.closest('table')) {
        case read_books:
            to_table = not_read;
            break;
        case not_read:
            to_table = read_books;
    }
    let new_row = to_table.insertRow(-1);
  
    Array.from(row_data).forEach((data) => {
        let cell = new_row.insertCell(-1);
        cell.innerHTML = data.innerHTML;
        row.remove();

    });

    let my_category = row.dataset.category,
        my_lit_type = row.dataset.litType;

    
    categories[my_category].innerHTML = parseInt(categories[my_category].innerHTML) + 1;
    lit_types[my_lit_type].innerHTML = parseInt(lit_types[my_lit_type].innerHTML) + 1;
    categories['total'].innerHTML = parseInt(categories['total'].innerHTML) + 1;

}


function drop_titles() {
    $.ajax({
        url: 'remove_all.php',
        contentType: 'application/x-www-form-urlencoded',
    });
    $('#read_books tr').remove();
    $('#total').html(0);
    for (const [key, value] of Object.entries(categories)) {
        value.innerHTML = 0;
    }
    for (const [key, value] of Object.entries(lit_types)) {
        value.innerHTML = 0;
    }
    
}


function sortTable(n) {
    let table;
    table = document.getElementById("table");
    var rows, i, x, y, count = 0;
    var switching = true;


    var direction = "ascending";

    while (switching) {
        switching = false;
        var rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            var Switch = false;

            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];

            if (direction == "ascending") {

                if (x.innerHTML.toLowerCase() > 
                y.innerHTML.toLowerCase()) {
                        

                    Switch = true;
                    break;
                }
            } else if (direction == "descending") {

                if (x.innerHTML.toLowerCase() < 
                y.innerHTML.toLowerCase()) {


                    Switch = true;
                    break;
                }
            }
        }
        if (Switch) {


            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;

            count++;
        } else {

            if (count == 0 && direction == "ascending") {
                direction = "descending";
                switching = true;
            }
        }
    }
}