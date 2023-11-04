<?php
$book_id = intval($_POST['id']);
$checked = strval($_POST['checked']);
require_once('functions.php');
require('login.php');

mysqli_select_db($conn,$dbname);
if ($checked === 'true') {
$sql = "INSERT INTO read_books (user_id, book_id)
        VALUES ('{$_SESSION['user_id']}', (SELECT book_id from tituly WHERE book_id = '$book_id') )";
} 

else if ($checked === 'false') {
$sql = "DELETE FROM read_books 
        WHERE user_id = '{$_SESSION['user_id']}' AND book_id = '$book_id'";
}

$result = mysqli_multi_query($conn,$sql);
?>