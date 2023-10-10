<?php 
session_start();

	include("connection.php");
	include("functions.php");
    
	if ($_SERVER['REQUEST_METHOD'] == "POST") {
		//something was posted
		$userName = $_POST['userName'];
		$userPassword = $_POST['userPassword'];

		if(!empty($userName) && !empty($userPassword) && !is_numeric($userName)) {

			//read from database
			$query = "select * from users where userName = '$userName' limit 1";
			$result = mysqli_query($conn, $query);

			if ($result) {
				if ($result && mysqli_num_rows($result) > 0) {

					$userData = mysqli_fetch_assoc($result);
					
					if ($userData['userPassword'] === $userPassword) {
                        $_SESSION['loggedin'] = true;
                        $_SESSION['userName'] = $userName;
						header("Location: http://localhost/odskrtavac/PHP/index.php");
						die;
					}
				}
			}
			
			echo "wrong username or password!";
		} else {
			echo "wrong username or password!";
		}
	}

?>

<?php include_once 'header.php'; ?>
    
    <main>
        <div class="table_wrapper">
			<form method="post">
				<input type="text" name="userName"><br>
				<input type="password" name="userPassword"><br>
				<input type="submit" value="Přihlásit se">
			</form>
        </div>
    </main>

    <script src="../JS/index.js";></script>
</body>
</html>