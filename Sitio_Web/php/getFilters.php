<?php
$conn = new mysqli("localhost", "root", "", "sonometro_iot");

if ($conn->connect_error) {
    die(json_encode(["error" => "Error de conexión a la base de datos."]));
}

// Perfiles
$profiles = [];
$result = $conn->query("SELECT idTipo AS id, nombreTipo AS name FROM tipo");
while ($row = $result->fetch_assoc()) {
    $profiles[] = $row;
}

// Usuarios
$users = [];
$result = $conn->query("SELECT idUsuario AS id, nombreUsuario AS name FROM usuario");
while ($row = $result->fetch_assoc()) {
    $users[] = $row;
}

// Direcciones
$directions = [];
$result = $conn->query("SELECT idDir AS id, tipoDir AS name FROM direcion");
while ($row = $result->fetch_assoc()) {
    $directions[] = $row;
}

echo json_encode(["profiles" => $profiles, "users" => $users, "directions" => $directions]);

$conn->close();
?>
