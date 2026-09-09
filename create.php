<?php
include 'db.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nome = $_POST['nome'];
    $email = $_POST['email'];

    $sql = "INSERT INTO usuarios (nome, email) VALUES ('$nome', '$email')";
    if ($conn->query($sql) === TRUE) {
        echo "Cadastro realizado!";
    } else {
        echo "Erro: " . $conn->error;
    }
}
?>
<form method="post">
  Nome: <input type="text" name="nome"><br>
  Email: <input type="email" name="email"><br>
  <button type="submit">Cadastrar</button>
</form>
