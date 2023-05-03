<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
	$para = "seu_email@provedor.com"; // substitua pelo seu endereço de e-mail
	$assunto = "Contato pelo Site";
	$nome = $_POST["nome"];
	$email = $_POST["email"];
	$mensagem = $_POST["mensagem"];
	$mensagem_formatada = "Nome: " . $nome . "\nE-mail: " . $email . "\nMensagem:\n" . $mensagem;
	mail($para, $assunto, $mensagem_formatada);
}

header('Location: index.html'); // redireciona o usuário para a página inicial

?>
