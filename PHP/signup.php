<?php require('connection.php'); require_once('header.php');

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
	$user_name = $_POST['user_name'];
	$user_password = $_POST['user_password'];

	if (!empty($user_name) && !empty($user_password) && !is_numeric($user_name)) {
		$query = "INSERT INTO users (user_name, user_password) 
				  VALUES ('$user_name','$user_password')";
		mysqli_query($conn, $query);
		header('Location: http://localhost/wtf/odskrtavac/PHP/index.php');
		exit;
	} else {
		echo 'Neplatné údaje!';
	}
}
?>
<main>
	<div class='form_wrapper'>
		<form method='POST'>
			<input type='text' name='user_name' placeholder='Zadejte jméno...'><br>
			<input type='password' name='user_password' placeholder='Zadejte heslo...'><br>
			<input type='submit' value='Registrovat se'>
		</form>
	</div>
</main>
<?php require_once('footer.php')?>