<?php
session_start();
    $_SESSION;
    include('functions.php')
?>

<?php include_once 'header.php'; ?>

    <main>
        <div class="table_wrapper">
            <div class="title"><a>Próza</a></div>
            <table>
                <tr>
                    <th>Autor</th>
                    <th>Název</th>
                    <th>Rok vydání</th>
                    <th>Původ</th>
                    <th></th>
                </tr>
            <?php
            $query = "SELECT autor, nazev, rok_vydani, puvod, literarni_druh FROM tituly";
            $result = mysqli_query($conn,$query);            

            while ($row = mysqli_fetch_assoc($result)) {
            echo "<tr>";
            echo "<td>" . $row["autor"] . "</td>";
            echo "<td>" . $row["nazev"] . "</td>";
            echo "<td>" . $row["rok_vydani"] . "</td>";
            echo "<td>" . $row["puvod"] . "</td>";
            echo "<td><input type='checkbox'></td>";
            echo "</tr>";                    
            }
            ?>
            </table>
        </div>
    </main>

    <script src="../JS/index.js";></script>
</body>
</html>