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
        <table id='not_read'>
            <tr>
                <th>Autor</th>
                <th>Název</th>
                <th>Rok vydání</th>
                <th>Původ</th>
                <th>Literární druh</th>
                <th>
                    <button  class='func_button' style='padding: 0;'>
                        <img src='../IMG/lupa.png' alt='lupa.png' style='width: 30px;'>
                    </button>
                </th>
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

                $autori = [];
                $autori[] = $autor;

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
        </table>
    
        <!--    Přečtené tituly    -->
    
        <h2 class='title'>Přečteno</h2>
        <table id='read_books'>
            <tr>
                <th>Autor</th>
                <th>Název</th>
                <th>Rok vydání</th>
                <th>Původ</th>
                <th>Literární druh</th>
                <th><button class='func_button' onclick='drop_titles()'>x</button></th>
            </tr>        
        <?php
        $query = "SELECT * FROM tituly
                  WHERE book_id IN (SELECT book_id FROM read_books WHERE user_id = {$_SESSION['user_id']})";
        $result = mysqli_query($conn,$query);
        if (mysqli_num_rows($result) != 0) {
        ?>
        

                <?php
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
            } else {
                $total = 0;
                echo 'nemáte přečtené žádné tituly';
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
                    <li id='total'>$total</li>
                    <li id='earlier_1800'>$earlier_1800</li>
                    <li id='earlier_1900'>$earlier_1900</li>
                    <li id='world'>$world</li>
                    <li id='czech'>$czech</li>
                    <ol id='types'>
                        <li id='prose'>$prose</li>
                        <li id='poetry'>$poetry</li>
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