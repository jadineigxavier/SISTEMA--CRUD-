<?php
$host = "sqlXXX.epizy.com";
$user = "usuario";
$pass = "senha";
$db   = "nome_do_banco";

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("Erro na conexão: " . $conn->connect_error);
}
?>
