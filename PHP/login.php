<?php 
require_once('functions.php');
    
	if ($_SERVER['REQUEST_METHOD'] == "POST") {
		$userName = $_POST['userName'];
		$userPassword = $_POST['userPassword'];

		if(!empty($userName) && !empty($userPassword) && !is_numeric($userName)) {

			$query = "SELECT * FROM users WHERE userName = '$userName' limit 1";
			$result = mysqli_query($conn, $query);

			if ($result) {
				if ($result && mysqli_num_rows($result) > 0) {

					$userData = mysqli_fetch_assoc($result);
					
					if ($userData['userPassword'] === $userPassword) {
                        $_SESSION['loggedin'] = true;
                        $_SESSION['userName'] = $userData['userName'];
                        $_SESSION['user_id'] = $userData['user_id'];
						$user_id = $_SESSION['user_id'];
						header('Location: http://localhost/test/odskrtavac/PHP/index.php');
						die;
					}
				}
			}
			
			echo "Neplatné údaje!";
		} else {
			echo "Špatné uživatelské jméno či heslo!";
		}
	}

require_once('header.php'); 
?>
    
    <main>
        <div class='table_wrapper'>
			<form method='POST'>
				<input type='text' name='userName'><br>
				<input type='password' name='userPassword'><br>
				<input type='submit' value='Přihlásit se'>
			</form>
        </div>
    </main>
</body>
</html>