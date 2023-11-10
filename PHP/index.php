<?php
require_once('header.php');
?>

<main>
<aside>
    <?php 
        echo "Světová a česká literatura do konce 18. století: ".sizeof($earlier_1800)."<br>";
        echo "Světová a česká literatura 19. století: ".sizeof($earlier_1900)."<br>";
        echo "Světová literatura 20. a 21. století: ".sizeof($world)."<br>";
        echo "Česká literatura 20. a 21. století: ".sizeof($czech)."<br>";
        echo "Próza:".sizeof($prose)."<br>";
        echo "Poezie: ".sizeof($poetry)."<br>";
        echo "Drama: ".sizeof($drama)."<br>";
    ?>
</aside>
    <div class='table_wrapper'>
        <table id='tituly'>
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
        </table>
        <table id='Přečteno'>
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