<?php

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "odskrtavac";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    exit("chyba: " . $conn->connect_error);
}
?>