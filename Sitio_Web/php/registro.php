<?php
header('Content-Type: application/json');
session_start();
$conn = new mysqli("localhost", "root", "", "sonometro_iot");

if ($conn->connect_error) {
    echo json_encode(["success" => false, "message" => "Error de conexión a la base de datos."]);
    exit();
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombreUsuario = $_POST['nombreUsuario'];
    $password = $_POST['password']; // Sin encriptar
    $tipo_idTipo = $_POST['tipo_idTipo'];

    $stmt = $conn->prepare("INSERT INTO usuario (nombreUsuario, password, tipo_idTipo) VALUES (?, ?, ?)");
    $stmt->bind_param("ssi", $nombreUsuario, $password, $tipo_idTipo);

    if ($stmt->execute()) {
        $_SESSION['user'] = $nombreUsuario;
        echo json_encode(["success" => true]);
    } else {
        echo json_encode(["success" => false, "message" => "Error al registrar el usuario."]);
    }

    $stmt->close();
} else {
    echo json_encode(["success" => false, "message" => "Método HTTP no válido."]);
}

$conn->close();
?>
