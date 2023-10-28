<?php
session_start();
    include('functions.php');
?>

<?php include_once 'header.php'; ?>

    <main>
        <div class="table_wrapper">
            <?php 
            create_table("Próza");
            create_table("Poezie");
            create_table("Drama")
            ?>
            <div class="table">
                <h1 class="title">Přečteno</h1>
                <table>
                    <tr>
                        <th>Autor</th>
                        <th>Název</th>
                        <th>Rok vydání</th>
                        <th>Původ</th>
                        <th></th>
                    </tr>
                    <?php
                    $button = "<td><input type='checkbox' onchange='handleChange(this)'";                    
                    $query = "SELECT book_id FROM read_books WHERE user_id = {$_SESSION['user_id']}";
                    $result = mysqli_query($conn,$query);
                    
                    while ($row = mysqli_fetch_assoc($result)) {
                        $query = "SELECT * FROM tituly WHERE book_id = '{$row['book_id']}'";
                        $tituly_result = mysqli_query($conn, $query);
                        while ($tituly_row = mysqli_fetch_assoc($tituly_result)) {
                            echo "
                            <tr>
                            <td>{$tituly_row['autor']}</td>
                            <td>{$tituly_row['nazev']}</td>
                            <td>{$tituly_row['rok_vydani']}</td>
                            <td>{$tituly_row['puvod']}</td>";
                            $fetch_read = "SELECT * FROM read_books WHERE user_id = {$_SESSION['user_id']} AND book_id = {$tituly_row['book_id']}";
                            echo $button; echo "id='{$tituly_row['book_id']}'";
                            if (mysqli_num_rows(mysqli_query($conn, $fetch_read)) > 0) {
                                echo "checked";
                            }
                            echo "></td>"; 
                            echo "</tr>";
                        }
                    }
                ?>
                </table>
            </div>
        </div>
    </main>

    <script src="../JS/index.js";></script>
</body>
</html>