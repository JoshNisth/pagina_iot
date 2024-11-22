<?php
$conn = new mysqli("localhost", "root", "", "sonometro_iot");

if ($conn->connect_error) {
    die(json_encode(["error" => "Error de conexión a la base de datos."]));
}

$result = $conn->query("
    SELECT fechaRegistro AS timestamp, nivelSonido1 AS value
    FROM registro
    ORDER BY fechaRegistro DESC
    LIMIT 10
");

$data = ["timestamps" => [], "values" => []];
while ($row = $result->fetch_assoc()) {
    $data["timestamps"][] = $row["timestamp"];
    $data["values"][] = $row["value"];
}

echo json_encode($data);

$conn->close();
?>
