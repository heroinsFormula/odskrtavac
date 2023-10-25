<?php
session_start();
    $_SESSION;
    include('functions.php');
?>

<?php include_once 'header.php'; ?>

    <main>
        <div class="table_wrapper">
            <div class="table">
                <h1 class="title">Próza</h1>
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Autor</th>
                        <th>Název</th>
                        <th>Rok vydání</th>
                        <th>Původ</th>
                        <th></th>
                    </tr>
                <?php
                $button = "<td><input type='checkbox' onchange='handleChange(this)'id=></td>";
                $query = "SELECT * FROM tituly WHERE literarni_druh='Próza'";
                $result = mysqli_query($conn,$query);
                while ($row = mysqli_fetch_assoc($result)) {
                    $book_id = $row["book_id"];
                echo "<tr>";
                echo "<td>" . $book_id . "</td>";
                echo "<td>" . $row["autor"] . "</td>";
                echo "<td>" . $row["nazev"] . "</td>";
                echo "<td>" . $row["rok_vydani"] . "</td>";
                echo "<td>" . $row["puvod"] . "</td>";
                $fetch_read = "SELECT * FROM read_books WHERE user_id = ".$_SESSION['user_id']." AND book_id = ".$book_id.""; // konečnězfhsadfk
                echo "<td><input type='checkbox' onchange='handleChange(this)' id='" . $book_id . "'";
                if (mysqli_num_rows(mysqli_query($conn, $fetch_read)) > 0) { // hnusný 
                    echo "checked";
                }
                echo "></td>"; 
                echo "</tr>";
                }
                ?>
                </table>
            </div>
            <div class="table">
                <h1 class="title">Drama</h1>
                <table>
                    <tr>
                        <th>Autor</th>
                        <th>Název</th>
                        <th>Rok vydání</th>
                        <th>Původ</th>
                        <th></th>
                    </tr>
                <?php
                $query = "SELECT * FROM tituly WHERE literarni_druh='Drama'";
                $result = mysqli_query($conn,$query);           
                
                while ($row = mysqli_fetch_assoc($result)) {
                echo "<tr>";
                echo "<td>" . $row["autor"] . "</td>";
                echo "<td>" . $row["nazev"] . "</td>";
                echo "<td>" . $row["rok_vydani"] . "</td>";
                echo "<td>" . $row["puvod"] . "</td>";
                echo $button;
                echo "</tr>";                    
                }
                ?>
                </table>
            </div>
            <div class="table">
                <h1 class="title">Poezie</h1>
                <table>
                    <tr>
                        <th>Autor</th>
                        <th>Název</th>
                        <th>Rok vydání</th>
                        <th>Původ</th>
                        <th></th>
                    </tr>
                <?php
                $query = "SELECT * FROM tituly WHERE literarni_druh='Poezie'";
                $result = mysqli_query($conn,$query);            

                while ($row = mysqli_fetch_assoc($result)) {
                echo "<tr>";
                echo "<td>" . $row["autor"] . "</td>";
                echo "<td>" . $row["nazev"] . "</td>";
                echo "<td>" . $row["rok_vydani"] . "</td>";
                echo "<td>" . $row["puvod"] . "</td>";
                echo $button;
                echo "</tr>";                    
                }
                ?>
                </table>
            </div>
        </div>
    </main>

    <script src="../JS/index.js";></script>
</body>
</html>