<?php require('connection.php');
$query = "DELETE FROM read_books
          WHERE user_id = {$_SESSION['user_id']}";
$result = mysqli_query($conn,$query);
?>