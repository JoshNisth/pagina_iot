<?php
session_start();
$conn = new mysqli("localhost", "root", "", "sonometro_iot");

header('Content-Type: application/json');

if ($conn->connect_error) {
    echo json_encode(['success' => false, 'message' => 'Error de conexión a la base de datos.']);
    exit();
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password']; // Sin verificar con hash

    // Preparar consulta para obtener usuario y verificar contraseña
    $stmt = $conn->prepare("SELECT * FROM usuario WHERE nombreUsuario = ? AND password = ?");
    $stmt->bind_param("ss", $username, $password);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $_SESSION['user'] = $username;
        echo json_encode(['success' => true, 'message' => 'Inicio de sesión exitoso.']);
    } else {
        echo json_encode(['success' => false, 'message' => 'Usuario o contraseña incorrectos.']);
    }

    $stmt->close();
} else {
    echo json_encode(['success' => false, 'message' => 'Método HTTP no válido.']);
}

$conn->close();
?>
