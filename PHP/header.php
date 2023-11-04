<?php require_once('functions.php'); ?>
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <meta name='author' content='Lukáš Ostrihoň'>
    <title>Odškrtávač</title>
    <link rel='stylesheet' type='text/css' media='screen' href='../CSS/main.css'>
    <script src='../JS/index.js'></script>
</head>
<body>
<header>
    <ul>
        <li><a href='index.php'>seznam děl</a></li>
        <li><a href=''>vlastní seznam</a></li>
        <li>
            <div id='login_wrap'>
            <?php
            if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] == true) {
                echo <<<HTML
                    <a>Vítejte uživateli {$_SESSION['userName']}</a>
                    <a href='logout.php'>odhlásit se</a>
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