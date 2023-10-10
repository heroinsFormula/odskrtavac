<?php
session_start();
$_SESSION['loggedin'] = false;
echo ("asdf");
session_unset();
session_destroy();
header("Location: login.php");
die;
?>