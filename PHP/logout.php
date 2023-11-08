<?php
require('connection.php');
$_SESSION['loggedin'] = false;
session_unset();
session_destroy();
header('Location: login.php');
die;
?>