<?php require('connection.php');
$_SESSION['logged_in'] = false;
session_unset();
session_destroy();
header('Location: login.php');
die;
?>