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
        create_read_table('Přečteno');
        ?>

    </div>
</main>
</body>
</html>