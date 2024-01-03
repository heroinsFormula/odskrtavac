<?php 
require('connection.php');
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <meta name='author' content='Lukáš Ostrihoň'>
    <title>Odškrtávač</title>
    <link rel='stylesheet' type='text/css' media='screen' href='../CSS/main.css'>
    <script src='https://code.jquery.com/jquery-3.7.1.min.js' integrity='sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=' crossorigin='anonymous'></script>
    <script src='../JS/index.js' defer></script>
</head>
<body>
<header>
    <ul>
        <li><a href='index.php'>seznam děl</a></li>
        <li><a href=''>vlastní seznam</a></li>
        <li><a href=''>vygenerovat studentský dokument</a></li>
        <li>
            <div id='login_wrap'>
            <?php
            if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] == true) {
                echo <<<HTML
                    <a>Vítejte uživateli {$_SESSION['userName']}</a>
                    <a href='logout.php'>odhlásit se</a>
                    <!-- <input type='color' value='#dedede' onchange='colorChange(this)'> -->
                HTML;
            } else {
                echo <<<HTML
                    <a href='login.php'>přihlásit se</a>
                    <a href='signup.php'>registrovat se</a>
                HTML;
            }
            ?>
            </div>
        </li>
    </ul>
</header>        