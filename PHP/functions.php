<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "odskrtavac";

$conn = new mysqli($servername, $username, $password, $dbname);

function create_table(string $type) {
global $conn;
echo"
<div class='table'>
    <h1 class='title'>{$type}</h1>
    <table>
        <tr>
            <th>Autor</th>
            <th>Název</th>
            <th>Rok vydání</th>
            <th>Původ</th>
            <th></th>
        </tr>";
        $button = "<td><input type='checkbox' onchange='handleChange(this)'";
        $query = "SELECT * FROM tituly WHERE literarni_druh='{$type}'";
        $result = mysqli_query($conn,$query);
        
        while ($row = mysqli_fetch_assoc($result)) {
            $book_id = $row["book_id"];
            
            echo "
            <tr>
            <td>{$row['autor']}</td>
            <td>{$row['nazev']}</td>
            <td>{$row['rok_vydani']}</td>
            <td>{$row['puvod']}</td>";
            $fetch_read = "SELECT * FROM read_books WHERE user_id = {$_SESSION['user_id']} AND book_id = {$book_id}";
            echo $button; echo "id='{$book_id}'";
            if (mysqli_num_rows(mysqli_query($conn, $fetch_read)) > 0) {
                echo "checked";
            }
            echo " 
            ></td> 
            </tr>"; // tohle furt vypadá docela nečitelně
        }
echo"   
    </table>
</div>";
}
?>