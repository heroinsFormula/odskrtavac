<?php 
session_start();

	include("connection.php");
	include_once("functions.php");


	if ($_SERVER['REQUEST_METHOD'] == "POST") {
		$userName = $_POST['userName'];
		$userPassword = $_POST['userPassword'];

		if (!empty($userName) && !empty($userPassword) && !is_numeric($userName)) {
			//save to database
			$query = "insert into users (userName, userPassword) values ('$userName','$userPassword')";
			mysqli_query($conn, $query);
            header('Location: http://localhost/test/odskrtavac/PHP/index.php');
            exit;
		} else {
			echo "Please enter some valid information!";
		}
	}
?>

<?php include_once 'header.php'; ?>
    
    <main>
        <div class="table_wrapper">
            <form method="post">
                <input type="text" name="userName"><br>
                <input type="password" name="userPassword"><br>
                <input type="submit" value="Registrovat se">
            </form>
        </div>
    </main>

    <script src="../JS/index.js";></script>
</body>
</html>