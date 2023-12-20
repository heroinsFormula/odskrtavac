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
let authors = [];


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
        cell.innerHTML = data.innerHTML; inner
        row.remove();

    });

    let my_category = row.dataset.category,
        my_lit_type = row.dataset.litType,
        my_author = row.dataset.author;


    authors.push(my_author);
    if ((new Set(authors)).size != authors.length) {
        console.log("fuck")
    }
    row.style.color = 'red';
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


let direction = 'ascending';
function sort_table(search_column) {
    var table = header_row.closest('table'),
        rows = table.rows,
        switching = true,
        i, cell1, cell2 = 0;

        

    
    while (switching) {
        switching = false;


        for (i = 1; i < (rows.length - 1); i++) {
            var Switch = false;

            cell1 = rows[i].getElementsByTagName('td')[search_column];
            cell2 = rows[i + 1].getElementsByTagName('td')[search_column];
            if (direction == 'ascending') {
                    if (cell1.innerHTML > cell2.innerHTML) {
                    // if (new Intl.Collator('cz').compare(cell1.innerHTML, cell2.innerHTML) < 0) {
                        Switch = true;
                        break;
                    }

            } else if (direction == 'descending') {
                if (cell1.innerHTML < cell2.innerHTML) {
                    // if (new Intl.Collator('cz').compare(cell1, cell2) < 0) {
                        Switch = true;
                        break;
                }
            }
        }

        if (Switch) {
            console.log("switching...", rows[i])
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;


        } else {
            if (direction == 'ascending') {
                direction = 'descending';
            }
            else {direction = 'ascending';}

        }
    }
};


function listen_up (listener, i) {
    listener.addEventListener('click',
        function() {
            sort_table(i);
        }
    );
}


let header_row = document.getElementById('header_row');
for (let i = 0; i < header_row.children.length; i++) {
    listen_up(header_row.children[i], i)
}


function openNav() {
    document.getElementById("myNav").style.width = "50%";
}


function closeNav() {
    document.getElementById("myNav").style.width = "0%";
}


// function colorChange(color) {
//     let root = document.documentElement;
//     console.log(root);
//     console.log(color.value);
//     root.style.setProperty('--color', color.value)
// }