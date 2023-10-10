<?php
session_start();
    $_SESSION;
?>

<?php include_once 'header.php'; ?>

    <main>cs
        <div class="table_wrapper">
            <div class="content">
                <div class="title"><a>Próza</a></div>
                <div class="table">tady bude tabulka</div>
                 <?php
                $servername = "localhost";
                $username = "root";
                $password = "";
                $dbname = "odskrtavac";

                $conn = new mysqli($servername, $username, $password, $dbname);

                    $sql = "SELECT * from tituly";
                    $test = $conn->query($sql);
                    echo $test;
                ?> 
            </div>
        </div>
    </main>

    <script src="../JS/index.js";></script>
</body>
</html>