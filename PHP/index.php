<?php
session_start();
    $_SESSION;
?>

<?php include_once 'header.php'; ?>

    <main>
        <div class="table_wrapper">
            <div class="content">
                <div class="title"><a>Próza</a></div>
                <div class="table">
                 <?php
                $servername = "localhost";
                $username = "root";
                $password = "";
                $dbname = "odskrtavac";

                $conn = new mysqli($servername, $username, $password, $dbname);

                $query = "SELECT autor, nazev, rok_vydani, puvod, literarni_druh FROM tituly";
                $result = mysqli_query($conn,$query);



                while ($row = mysqli_fetch_assoc($result)) {
                echo "autor: " . $row["autor"]. " ";
                echo "Název: " . $row["nazev"]. " ";
                echo "rok vydani " . $row["rok_vydani"]."<br>";
                }


                ?>
                </div>
            </div>
        </div>
    </main>

    <script src="../JS/index.js";></script>
</body>
</html>