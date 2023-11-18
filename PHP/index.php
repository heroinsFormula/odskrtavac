<?php
require_once('header.php');
require_once('functions.php');
?>

<main>
    <?php
    if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] == false) {
        echo <<<HTML
            <a>Pro užití stránky se nejdřív musíte příhlásit</a>
        HTML;
    } else {
    ?>
    <button onclick='openNav()' style='position: sticky; top: 50%;'>ahoj</button>
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
                $autor = $row['autor'];
                $rok = $row['rok_vydani'];
                $puvod = $row['puvod'];
                $druh = $row['literarni_druh'];
                $cat = '';
                $type = '';

                switch (true) {
                    case $rok <= 1800: // $rok = xxxx-1800
                        $cat = 'earlier_1800';
                        break;
                    case $rok <= 1900: // $rok = 1801-1900
                        $cat = 'earlier_1900';
                        break;
                    default:
                        $puvod === 'Česká republika' ? $cat = 'czech' : $cat = 'world';
                }
                
                switch ($druh) {
                    case 'Próza':
                        $type = 'prose';   
                        break;
                    case 'Poezie':
                        $type = 'poetry';
                        break;
                    case 'Drama':
                        $type = 'drama';
                        break;
                }

            echo <<<HTML
                    <tr data-category='$cat' data-lit-type='$type'>
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

            <!--    Přečtené tituly    -->
            <tr class='title'>
                <td style='border-width: 0px;'>Přečteno</td>
            </tr>
            <tr>
                <th>Autor</th>
                <th>Název</th>
                <th>Rok vydání</th>
                <th>Původ</th>
                <th>Literární druh</th>
                <th><button onclick='drop_titles()'>x</button></th>
            </tr>
            <?php
            $query = "SELECT * FROM tituly
                      WHERE book_id IN (SELECT book_id FROM read_books WHERE user_id = {$_SESSION['user_id']})";
            $result = mysqli_query($conn,$query);
            if (mysqli_num_rows($result) != 0) {
    
                while ($row = mysqli_fetch_assoc($result)) {
                    $book_id = $row['book_id'];
                    $autor = $row['autor'];
                    $rok = $row['rok_vydani'];
                    $puvod = $row['puvod'];
                    $druh = $row['literarni_druh'];
                    $total = mysqli_num_rows($result);

                    switch (true) {
                        case $rok <= 1800: // $rok = xxxx-1800
                            $earlier_1800 += 1;
                            break;
                        case $rok <= 1900: // $rok = 1801-1900
                            $earlier_1900 += 1;
                            break;
                        default:
                            $puvod === 'Česká republika' ? $czech += 1 : $world += 1;
                    }
                    
                    switch ($druh) {
                        case 'Próza':
                            $prose += 1;   
                            break;
                        case 'Poezie':
                            $poetry += 1;
                            break;
                        case 'Drama':
                            $drama += 1;
                            break;
                    }

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
                $total = 0;
            }
            ?>
        </table>
        
    </div>
    <div id="myNav" class="overlay">
        <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
        <div class="overlay-content">
            <?php
            echo <<<HTML
                <h1 style='color:white;'>Kritéria pro výběr literárních děl do seznamu k maturitní zkoušce:</h1>
                <ol id='criteria'>
                    <label for='total'>Počet literárních děl žákovského seznamu: 20</label>
                    <li id='total'>$total</li>
                    <label for='earlier_1800'>Světová a česká literatura do konce 18. století (min. 2 díla):</label>
                    <li id='earlier_1800'>$earlier_1800</li>
                    <label for='earlier_1900'>Světová a česká literatura 19. století (min. 3 díla): </label>
                    <li>$earlier_1900</li>
                    <label for='world'>Světová literatura 20. a 21. století (min. 4 díla): </label>
                    <li id='world'>$world</li>
                    <label for='czech'>Česká literatura 20. a 21. století (min. 5 děl): </label>
                    <li id='czech'>$czech</li>
                    <label for='types'>Minimálně dvěma literárními díly musí být v seznamu žáka zastoupena:</label>
                    <ol id='types'>
                        <label for='prose'>Próza: </label>
                        <li id='prose'>$prose</li>
                        <label for='poetry'>Poezie: </label>
                        <li id='potery'>$poetry</li>
                        <label for='drama'>Drama: </label>
                        <li id='drama'>$drama</li>
                    </ol>
                </ol>
            HTML;
        }
            ?>
        </div>

    </div>
</main>
</body>
</html>