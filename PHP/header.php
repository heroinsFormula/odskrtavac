<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <title>Odškrtávač</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <link rel='stylesheet' type='text/css' media='screen' href='../CSS/main.css'>
    <script src='../JS/index.js'></script>
</head>
<body>
<header>
    <ul>
        <li><a href="index.php">seznam děl</a></li>
        <li><a href="#">vlastní seznam</a></li>
        <li><div id="login_wrap">
        <?php
        if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] == true) {
            echo(
            "<ps>vítejte uživateli </a>" . htmlspecialchars($_SESSION['userName']).
            "<a href='logout.php'>odhlásit se</a>");
        } else {
            echo(
            "<a href='login.php'>přihlásit se</a>".
            "<a href='signup.php'>registrovat se</a>");
        }?>
        </div></li>
    </ul>
</header>        