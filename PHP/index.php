<?php require_once('header.php'); require_once('functions.php'); ?>

<main>
<?php
if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] == false) {
    echo <<<HTML
    <div class='form_wrapper'>
        <a style='color: black;'>Pro použití stránky se nejdřív musíte příhlásit</a>
    </div>
    HTML;
} else {
?>
<button onclick='openNav()' style='position: fixed; transform: translateY(-50%); top: 50%;'>></button>
<div class='table_wrapper'>
    <table>
    <thead>
    <tr id='header_row'>
        <th>Autor</th>
        <th>Název</th>
        <th>Rok vydání</th>
        <th>Původ</th>
        <th>Literární druh</th>
        <th>
            <button class='search_button' onclick='search_menu_open()'>
                <img src='../IMG/lupa.svg' alt='lupa.svg' style='width: 30px;'>
            </button>
        </th>
    </tr>
    </thead>
    <tbody>
    <?php
    $query = "SELECT * FROM tituly
              WHERE book_id NOT IN (SELECT book_id FROM read_books)";
    $result = mysqli_query($conn, $query);
    
    while ($row = mysqli_fetch_assoc($result)) {
        $book_id = $row['book_id'];
        $autor = $row['autor'];
        $nazev = $row['nazev'];
        $rok = $row['rok_vydani'];
        $puvod = $row['puvod'];
        $druh = $row['literarni_druh'];
        $category = '';
        $type = '';
        $flag = $flags[$puvod];
        // $před_naším_letopočtem = '';
    

        // if ($rok < 0) { !NEFUNGUJE SORT_TABLE() S ABSOLUTNÍ HODNOTOU!
        //     $rok = abs($rok);
        //     $před_naším_letopočtem = ' př. n. l.';  
        // }

        switch (true) {
            case $rok <= 1800: // $rok = xxxx-1800
                $category = 'earlier_1800';
                break;
            case $rok <= 1900: // $rok = 1801-1900
                $category = 'earlier_1900';
                break;
            default:
                $puvod === 'Česká republika' ? $category = 'czech' : $category = 'world';
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
            <tr data-category='$category' data-lit-type='$type' data-author='$autor'>
                <td>$autor</td>
                <td>$nazev</td>
                <td>$rok</td>
                <td><span class='text'>$puvod</span>
                    <img style='float: right;' class='icon' 
                         src='../IMG/flags/4x3/$flag' width='24' height='18' alt='$flag'>
                </td>
                <td>$druh</td>
                <td><input type='checkbox' onchange='handle_change(this)' id='$book_id'></td>
            </tr>
        HTML;
    }


$query = "SELECT * FROM tituly
          WHERE book_id IN 
          (SELECT book_id FROM read_books 
           WHERE user_id = {$_SESSION['user_id']}
           )";
$result = mysqli_query($conn,$query);

    while ($row = mysqli_fetch_assoc($result)) {
        $book_id = $row['book_id'];
        $autor = $row['autor'];
        $nazev = $row['nazev'];
        $rok = $row['rok_vydani'];
        $puvod = $row['puvod'];
        $druh = $row['literarni_druh'];
        $category = '';
        $type = '';
        $total = mysqli_num_rows($result);
        $flag = $flags[$puvod];
        $před_naším_letopočtem = '';

        $autori[] = $autor;

        // if ($rok < 0) {
        //     $rok = abs($rok);
        //     $před_naším_letopočtem = ' př. n. l.';
        // }

        switch (true) {
            case $rok <= 1800: // $rok = xxxx-1800
                $earlier_1800 += 1;
                $category = 'earlier_1800';
                break;
            case $rok <= 1900: // $rok = 1801-1900
                $earlier_1900 += 1;
                $category = 'earlier_1900';
                break;
            default:
                if ($puvod === 'Česká republika') {
                    $czech += 1;
                    $category = 'czech';
                } else {
                    $world += 1;
                    $category = 'world';
                }
        }
        
        switch ($druh) {
            case 'Próza':
                $prose += 1;
                $type = 'prose';
                break;
            case 'Poezie':
                $poetry += 1;
                $type = 'poetry';
                break;
            case 'Drama':
                $drama += 1;
                $type = 'drama';
                break;
        }

        echo <<<HTML
            <tr data-category='$category' data-lit-type='$type' data-author='$autor'>
                <td>$autor</td>
                <td>$nazev</td>
                <td>$rok</td>
                <td><span class='text'>$puvod</span>
                    <img style='float: right;' class='icon' 
                         src='../IMG/flags/4x3/$flag' width='24' height='18' alt='$flag'>
                </td>
                <td>$druh</td>
                <td><input type='checkbox' onchange='handle_change(this)' id='$book_id' checked></td>
            </tr>
        HTML;
    }
    $js_autori = json_encode($autori);
    ?>
    </tbody>
    </table>
    <script>
        let autori = <?php echo $js_autori ?>
    </script>
    
</div>
<div id="myNav" class="overlay">
    <a href="javascript:void(0)" class="close_button" onclick="closeNav()">&times;</a>
    <div class="overlay-content">
        <?php
        echo <<<HTML
            <h1 style='color:white;'>Kritéria pro výběr literárních děl do seznamu k maturitní zkoušce:</h1>
            <ol id='criteria'>
                <label for='total'>Celkem přečtených děl:</label>
                <li id='total'>$total</li>
                <label for='earlier_1800'>18. století a dřív:</label>
                <li id='earlier_1800'>$earlier_1800</li>
                <label for='earlier_1900'>19. století a dřív:</label>
                <li id='earlier_1900'>$earlier_1900</li>
                <label for='world'>Světová literatura z 20. a 21. století:</label>
                <li id='world'>$world</li>
                <label for='czech'>Česká literatura z 20. a 21. století:</label>
                <li id='czech'>$czech</li>
                    <label for='prose'>Próza:</label>
                    <li id='prose'>$prose</li>
                    <label for='poetry'>Poezie:</label>
                    <li id='poetry'>$poetry</li>
                    <label for='drama'>Drama:</label>
                    <li id='drama'>$drama</li>
                <li id='author_condition'>Od jednoho autora mohou být zvolena max. 2 literární díla.</li>
            </ol>
            <h2>Status: <span id='status'>Nesplněno</span></h2>
    </div>
</div>
<div id='search_menu'>
    <div id='search_menu_content'>
        <a href="javascript:void(0)" class="close_button" onclick="search_menu_close()">&times;</a>
        <div><input type='text' placeholder='Najít titul..'></div>
        <div><input type='checkbox'><input type='checkbox'></div>
        <div><input type='checkbox'><input type='checkbox'></div>
    </div>
</div>
HTML;
}
?>
</main>
<?php require_once('footer.php')?>