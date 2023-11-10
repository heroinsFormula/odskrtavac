<?php
require_once('header.php');
require_once('functions.php');
print_r($_SESSION);
?>

<main>
    <div id="myNav" class="overlay">
    
        <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
        <div class="overlay-content">
            <?php
            echo <<<HTML
                    <a>Světová a česká literatura do konce 18. století: $earlier_1800</a>
                    <a>Světová a česká literatura 19. století: $earlier_1900</a>
                    <a>Světová literatura 20. a 21. století: $world</a>
                    <a>Česká literatura 20. a 21. století: $czech</a>
                    <a>Próza: $prose</a>
                    <a>Poezie: $poetry</a>
                    <a>Drama: $drama</a>
                    <a>Celkem: $total</a>
            HTML;
            ?>
        </div>

    </div>
    <button onclick='openNav()' style='position: sticky; top: 50%;' img='src url(../IMG/lupa.png)'>ahoj</button>
    <div class='table_wrapper'>
        <table id='tituly'>
            <tr>
                <th>Autor</th>
                <th>Název</th>
                <th>Rok vydání</th>
                <th>Původ</th>
                <th>Literární druh</th>
                <th><button><img src='../IMG/lupa.png' id='search_button'></button></th>
            </tr>
            
            <?php
            $query = "SELECT * FROM tituly
                      WHERE book_id NOT IN (SELECT book_id FROM read_books)";
            $result = mysqli_query($conn,$query);
            
            while ($row = mysqli_fetch_assoc($result)) {
                $book_id = $row['book_id'];
                echo <<<HTML
                    <tr>
                        <td>{$row['autor']}</td>
                        <td>{$row['nazev']}</td>
                        <td>{$row['rok_vydani']}</td>
                        <td>{$row['puvod']}</td>
                        <td>{$row['literarni_druh']}</td>
                        <td><input type='checkbox' onchange='handleChange(this)' id='$book_id'></td>
                    </tr>
                HTML;
            }
            ?>
            <tr class='title'>
                <td style='border-width: 0px;'>Přečteno</td>
            </tr>
            <tr>
                <th>Autor</th>
                <th>Název</th>
                <th>Rok vydání</th>
                <th>Původ</th>
                <th>Literární druh</th>
                <th></th>
            </tr>
            <?php
            $query = "SELECT * FROM tituly
                      WHERE book_id IN (SELECT book_id FROM read_books WHERE user_id = {$_SESSION['user_id']})";
            $result = mysqli_query($conn,$query);
            if (mysqli_num_rows($result) != 0) {
    
                while ($row = mysqli_fetch_assoc($result)) {
                    $book_id = $row['book_id'];
                    echo <<<HTML
                        <tr>
                            <td>{$row['autor']}</td>
                            <td>{$row['nazev']}</td>
                            <td>{$row['rok_vydani']}</td>
                            <td>{$row['puvod']}</td>
                            <td>{$row['literarni_druh']}</td>
                            <td><input type='checkbox' onchange='handleChange(this)' id='$book_id' checked></td>
                        </tr>
                    HTML;
                }
                echo <<<HTML
                    </table>
                    </div>
                HTML;

            } else {
                
            }
            ?>
        </table>
    </div>
</main>
</body>
</html>