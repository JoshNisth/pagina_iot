<?php
$conn = new mysqli("localhost", "root", "", "sonometro_iot");

if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

$result = $conn->query("SELECT idTipo, nombreTipo FROM tipo");
$options = "";

while ($row = $result->fetch_assoc()) {
    $options .= "<option value='" . htmlspecialchars($row['idTipo']) . "'>" . htmlspecialchars($row['nombreTipo']) . "</option>";
}

echo $options;

$conn->close();
?>
