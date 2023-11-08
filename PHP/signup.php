<?php 
require_once('functions.php');


	if ($_SERVER['REQUEST_METHOD'] == 'POST') {
		$userName = $_POST['userName'];
		$userPassword = $_POST['userPassword'];

		if (!empty($userName) && !empty($userPassword) && !is_numeric($userName)) {
			$query = "INSERT INTO users (userName, userPassword) VALUES ('$userName','$userPassword')";
			mysqli_query($conn, $query);
            header('Location: http://localhost/test/odskrtavac/PHP/index.php');
            exit;
		} else {
			echo 'Neplatné údaje!';
		}
	}

require_once('header.php');
?>
    
	<main>
		<div class='table_wrapper'>
			<form method='post'>
				<input type='text' name='userName'><br>
				<input type='password' name='userPassword'><br>
				<input type='submit' value='Registrovat se'>
			</form>
		</div>
	</main>
</body>
</html>