<?php
$book_id = intval($_GET['id']);
include("functions.php");
if (!$conn) {
    die('Could not connect: ' . mysqli_error($con));
  }
mysqli_select_db($conn,"odskrtavac");
$sql="INSERT INTO read_books(book_id) SELECT book_id FROM tituly WHERE book_id = '".$book_id."'";
$result = mysqli_query($conn,$sql);
?>