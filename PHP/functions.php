<?php
require('connection.php');


function create_header($table_name) {
    echo <<<HTML
    <div class='table'>
    <h1 class='title'>$table_name</h1>
    <table id='$table_name'>
        <tr>
            <th>Autor</th>
            <th>Název</th>
            <th>Rok vydání</th>
            <th>Původ</th>
            <th></th>
        </tr>
    HTML;
}


function create_table(string $lit_druh) {
        global $conn;

        $query = "SELECT * FROM tituly 
                  WHERE literarni_druh='$lit_druh' 
                  AND book_id NOT IN (SELECT book_id FROM read_books)";
        $result = mysqli_query($conn,$query);
        
        if (mysqli_num_rows($result) != 0) {
        create_header($lit_druh);

        while ($row = mysqli_fetch_assoc($result)) {
            $book_id = $row['book_id'];
            $fetch_read = "SELECT * FROM read_books 
                           WHERE user_id = {$_SESSION['user_id']} 
                           AND book_id = '$book_id'";
            $fetch_result = mysqli_query($conn, $fetch_read);
            $checked = NULL;
            (mysqli_num_rows($fetch_result) == 1) ? $checked = 'checked' : null;
            
            echo <<<HTML
                <tr data-lit-druh='$lit_druh'>
                    <td>{$row['autor']}</td>
                    <td>{$row['nazev']}</td>
                    <td>{$row['rok_vydani']}</td>
                    <td>{$row['puvod']}</td>
                    <td><input type='checkbox' onchange='handleChange(this)' id='$book_id' $checked></td>
                </tr>
            HTML;
        }

        echo <<<HTML
            </table>
            </div>
        HTML;
    }
}


function create_read_table($title) {
        global $conn;

        $query = "SELECT * FROM tituly
                  WHERE book_id IN (SELECT book_id FROM read_books WHERE user_id = {$_SESSION['user_id']})";
        $result = mysqli_query($conn,$query);
        if (mysqli_num_rows($result) != 0) {
            create_header($title);
            
            while ($row = mysqli_fetch_assoc($result)) {
                $book_id = $row['book_id'];
                echo <<<HTML
                    <tr data-lit-druh=''>
                        <td>{$row['autor']}</td>
                        <td>{$row['nazev']}</td>
                        <td>{$row['rok_vydani']}</td>
                        <td>{$row['puvod']}</td>
                        <td><input type='checkbox' onchange='handleChange(this)' id='$book_id' checked></td>
                    </tr>
                HTML;
            }

        echo <<<HTML
            </table>
            </div>
        HTML;
    }
}



?>