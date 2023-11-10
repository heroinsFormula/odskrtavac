<?php
!isset($_SESSION) ? session_start() : null;
$servername = 'localhost';
$username = 'root';
$password = '';
$dbname = 'odskrtavac';

$conn = new mysqli($servername, $username, $password, $dbname);

!$conn ? exit("chyba: $conn") : null;
?>