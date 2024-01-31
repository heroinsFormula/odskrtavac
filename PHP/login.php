<?php require('connection.php'); require_once('header.php');
    
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
	$user_name = $_POST['user_name'];
	$user_password = $_POST['user_password'];

	if(!empty($user_name) && !empty($user_password) && !is_numeric($user_name)) {

		$query = "SELECT * FROM users WHERE user_name = '$user_name' limit 1";
		$result = mysqli_query($conn, $query);

		if ($result) {
			if ($result && mysqli_num_rows($result) > 0) {

				$userData = mysqli_fetch_assoc($result);
				
				if ($userData['user_password'] === $user_password) {
					$_SESSION['logged_in'] = true;
					$_SESSION['user_name'] = $userData['user_name'];	
					$_SESSION['user_id'] = $userData['user_id'];
					header('Location: http://localhost/wtf/odskrtavac/PHP/index.php');
					die;
				}
			}
		}
		
		echo "Neplatné údaje!";
	} else {
		echo "Špatné uživatelské jméno či heslo!";
	}
}
?>
    
    <main>
        <div class='form_wrapper'>
			<form method='POST'>
				<input type='text' name='user_name' placeholder='Zadejte jméno...'><br>
				<input type='password' name='user_password' placeholder='Zadejte heslo...'><br>
				<input type='submit' value='Přihlásit se'>
			</form>
        </div>
    </main>
<?php require_once('footer.php')?>