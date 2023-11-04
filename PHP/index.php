<?php
session_start();
require_once('header.php');
?>

<main>
    <div class='table_wrapper'>
        <?php 
        create_table('Próza');
        create_table('Poezie');
        create_table('Drama');
        
        $query = "SELECT book_id FROM read_books 
                  WHERE user_id = {$_SESSION['user_id']}";
        $result = mysqli_query($conn,$query);
        if (mysqli_num_rows($result) != 0 ) {
        echo <<<HTML
            <div class='table'>
            <h1 class='title'>Přečteno</h1>
            <table>
                <tr>
                    <th>Autor</th>
                    <th>Název</th>
                    <th>Rok vydání</th>
                    <th>Původ</th>
                    <th></th>
                </tr>
            HTML;
                while ($row = mysqli_fetch_assoc($result)) {
                    $tituly_query = "SELECT * FROM tituly 
                                     WHERE book_id = '{$row['book_id']}'";
                    $tituly_result = mysqli_query($conn, $tituly_query);
                    while ($tituly_row = mysqli_fetch_assoc($tituly_result)) {
                        echo <<<HTML
                            <tr>
                                <td>{$tituly_row['autor']}</td>
                                <td>{$tituly_row['nazev']}</td>
                                <td>{$tituly_row['rok_vydani']}</td>
                                <td>{$tituly_row['puvod']}</td>
                                <td><input type='checkbox' onchange='handleChange(this)' checked>
                            </tr>
                        HTML;
                    }
                }
        echo <<<HTML
            </table>
            </div>
        HTML;
        } else {
            // uživatel nemá nic přečteno
        }
        ?>

    </div>
</main>
</body>
</html>