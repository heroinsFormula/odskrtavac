<?php
$book_id = intval($_POST['id']);
$checked = strval($_POST['checked']);
include("functions.php");
if (!$conn) {
    die('Could not connect: ' . mysqli_error($con));
  }
mysqli_select_db($conn,"odskrtavac");
if ($checked === "true") {
$sql="INSERT INTO read_books(book_id) SELECT book_id FROM tituly WHERE book_id = '".$book_id."'";
} 
else if ($checked === "false") {
$sql="INSERT INTO read_books(read_book) VALUES('".$checked."')";
}

$result = mysqli_query($conn,$sql);
?>