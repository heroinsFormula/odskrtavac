<?php
require('connection.php');
$query = "SELECT * FROM tituly
          WHERE book_id IN (SELECT book_id FROM read_books WHERE user_id = {$_SESSION['user_id']})";
$result = mysqli_query($conn,$query);

$total = mysqli_num_rows($result);
$earlier_1800 = array(); // xxxx-1800
$earlier_1900 = array(); // 1801-1900
$czech = array(); // 1901-2000
$world = array(); 
$prose = array();
$poetry = array();
$drama = array();

while ($row = mysqli_fetch_assoc($result)) {
    $autor = $row['autor'];
    $rok = $row['rok_vydani'];
    $puvod = $row['puvod'];
    $druh = $row['literarni_druh'];

    if ($rok < 1800) {
        $earlier_1800[] = $rok;
    } elseif ($rok < 1900){
        $earlier_1900[] = $rok;
    } elseif ($puvod == 'Česká republika') {
        $czech[] = $rok;
    } else {
        $world[] = $rok;
    }
    
    switch ($druh) {
        case 'Próza':
            $prose[] = $druh;   
            break;
        case 'Poezie':
            $poetry[] = $druh;
            break;
        case 'Drama':
            $drama[] = $druh;
            break;
    }
}

$earlier_1800 = sizeof($earlier_1800);
$earlier_1900 = sizeof($earlier_1900);
$czech = sizeof($czech);
$world = sizeof($world);
$prose = sizeof($prose);
$poetry = sizeof($poetry);
$drama = sizeof($drama);
?>