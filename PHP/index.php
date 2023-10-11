<?php
session_start();
    $_SESSION;
    include('functions.php')
?>

<?php include_once 'header.php'; ?>

    <main>
        <div class="table_wrapper">
            <div class="content">
                <div class="title"><a>Próza</a></div>
                <div class="table">
                 <?php

                $query = "SELECT autor, nazev, rok_vydani, puvod, literarni_druh FROM tituly";
                $result = mysqli_query($conn,$query);




            

    
                ?>
                <table>
                    <tr>
                        <th>Autor</th>
                        <th>Název</th>
                        <th>Rok vydání</th>
                        <th>Původ</th>
                    </tr>
                <?php while ($row = mysqli_fetch_assoc($result)) {
                echo "<tr>";
                echo "<td>" . $row["autor"] . "</td>";
                echo "<td>" . $row["nazev"] . "</td>";
                echo "<td>" . $row["rok_vydani"] . "</td>";
                echo "<td>" . $row["puvod"] . "</td>";
                echo "</tr>";                    
                }
                ?>
                    </table>
                    
                </div>
            </div>
        </div>
    </main>

    <script src="../JS/index.js";></script>
</body>
</html>