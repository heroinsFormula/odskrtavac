<?php
require('connection.php');

function create_table(string $lit_druh) {
global $conn;
echo <<<HTML
    <div class='table'>
    <h1 class='title'>$lit_druh</h1>
    <table>
        <tr>
            <th>Autor</th>
            <th>Název</th>
            <th>Rok vydání</th>
            <th>Původ</th>
            <th></th>
        </tr>
    HTML;
    
    $query = "SELECT * FROM tituly 
              WHERE literarni_druh='$lit_druh'";
    $result = mysqli_query($conn,$query);
    while ($row = mysqli_fetch_assoc($result)) {
        $book_id = $row['book_id'];
        $fetch_read = "SELECT * FROM read_books 
                       WHERE user_id = {$_SESSION['user_id']} AND book_id = '$book_id'";
        $checked = NULL;
        if (mysqli_num_rows(mysqli_query($conn, $fetch_read)) == 1) {
            $checked = 'checked';
        }
        
        echo <<<HTML
        
            <tr>
                <td>{$row['autor']}</td>
                <td>{$row['nazev']}</td>
                <td>{$row['rok_vydani']}</td>
                <td>{$row['puvod']}</td>
                <td><input type='checkbox' onchange='handleChange(this)' id='{$book_id}' $checked></td>
            </tr>
        HTML;
    }

echo <<<HTML
    </table>
    </div>
HTML;
}

?>