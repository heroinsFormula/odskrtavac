<?php
session_start();
$servername = 'localhost';
$username = 'root';
$password = '';
$dbname = 'odskrtavac';

$conn = new mysqli($servername, $username, $password, $dbname);

if (!$conn) {exit("chyba: $conn");}
?>