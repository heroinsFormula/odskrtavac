let categories = {
    earlier_1800 : document.getElementById('earlier_1800'),
    earlier_1900 : document.getElementById('earlier_1900'),
    world : document.getElementById('world'),
    czech : document.getElementById('czech'),
    'total' : document.getElementById('total'),
    author_condition : document.getElementById('author_condition'),
}

let lit_types = {
    prose : document.getElementById('prose'),
    poetry : document.getElementById('poetry'),
    drama : document.getElementById('drama'),
}

function get_duplicates() {
    const duplicates = [];
    for (let i = 0; i < autori.length; i++) {
        for (let j = i + 1; j < autori.length; j++) {
          if (autori[i] === autori[j] || autori[i] in duplicates) {
            duplicates.push(autori[i]);
          }
        }
    }

    if (duplicates.length > 2) {
        duplicates.forEach((autor) => {
            let red_rows = document.querySelectorAll(`[data-author="${autor}"]`);
            red_rows.forEach((row) => {
            row.style.color = 'red';
            change_status('Máte od jednoho autora více titulů!', author_condition)
            })
        })
    }
    else if (duplicates.length < 2) {
        duplicates.forEach((autor) => {
            let red_rows = document.querySelectorAll(`[data-author="${autor}"]`);
            red_rows.forEach((row) => {
            row.style.color = 'black';
            change_status('OK', author_condition)
            })
        })
    }
}


function handle_change(checkbox) {
    // let params = `id=${checkbox.id}`;
    // checkbox.checked ? params += `&checked=true` : params += `&checked=false`;
    // xhttp.open('POST', 'add_to_db.php');
    // xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    // xhttp.send(params);
    console.log('before', autori)
    $.ajax({
        type: 'POST',
        url: 'add_to_db.php',
        data: jQuery.param({ id: `${checkbox.id}`, checked : `${checkbox.checked}`}) ,
        contentType: 'application/x-www-form-urlencoded',
    });



    let row = checkbox.closest('tr'),
        table = row.closest('tbody');

    let my_category = row.dataset.category,
        my_lit_type = row.dataset.litType,
        my_author = row.dataset.author;
        console.log(my_category, my_lit_type, my_author)

    if (checkbox.checked) {
        previous_row = row.rowIndex - 1;
        table.insertBefore(row, null)

        categories[my_category].innerHTML = parseInt(categories[my_category].innerHTML) + 1;
        lit_types[my_lit_type].innerHTML = parseInt(lit_types[my_lit_type].innerHTML) + 1;
        categories['total'].innerHTML = parseInt(categories['total'].innerHTML) + 1;
        autori.push(my_author);

    } else if (!checkbox.checked) {
        if (typeof previous_row === 'undefined') {
            previous_row = row // Fallback při obnovení stránky
        }
        table.insertBefore(row, table.rows[previous_row])

        categories[my_category].innerHTML = parseInt(categories[my_category].innerHTML) - 1;
        lit_types[my_lit_type].innerHTML = parseInt(lit_types[my_lit_type].innerHTML) - 1;
        categories['total'].innerHTML = parseInt(categories['total'].innerHTML) - 1;
        idx = autori.indexOf(my_author);
        if (idx != -1) autori.splice(idx, 1);
    }
    console.log('after', autori)
    get_duplicates()
   

}


let _status = document.getElementById('status') // Bez podtržídka to mění Window.status
function change_status(status_message, offending_category) {
    if (status_message === 'OK') {
        _status.innerHTML = 'Nesplněno';
        offending_category.style.color = 'white';
        return
    }
    _status.innerHTML = status_message;
    offending_category.style.color = 'red';

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
            cell_texts = [cell1.innerHTML, cell2.innerHTML]
            if (direction == 'ascending') {
                    if (cell1.innerHTML > cell2.innerHTML) {
                    // if (cell_texts != cell_texts.sort(Intl.Collator('cz').compare)) {
                        Switch = true;
                        break;
                    }

            } else if (direction == 'descending') {
                if (cell1.innerHTML < cell2.innerHTML) {
                    // if (cell_texts != cell_texts.sort(Intl.Collator('cz').compare)) {
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
for (let i = 0; i < header_row.children.length-1; i++) {
    listen_up(header_row.children[i], i)
}


function openNav() {
    document.getElementById('myNav').style.width = '50%';
}


function closeNav() {
    document.getElementById('myNav').style.width = '0%';
}


// function colorChange(color) {
//     let root = document.documentElement;
//     console.log(root);
//     console.log(color.value);
//     root.style.setProperty('--color', color.value)
// }
function search_menu_open() {
    document.getElementById('search_menu').style.display = 'block';
}

function search_menu_close() {
    document.getElementById('search_menu').style.display = 'none';
}

get_duplicates()
