<?php
header('Content-Type: application/json');

$conn = new mysqli("localhost", "root", "", "sonometro_iot");

if ($conn->connect_error) {
    die(json_encode(["error" => "Error de conexión a la base de datos."]));
}

// Consulta para obtener la cantidad por dirección
$query = "
    SELECT d.tipoDir AS direccion, COUNT(r.idRegistro) AS cantidad
    FROM registro r
    INNER JOIN direcion d ON r.direcion_idDir = d.idDir
    GROUP BY d.tipoDir
    ORDER BY cantidad DESC
";

$result = $conn->query($query);

$data = ["labels" => [], "values" => []];
while ($row = $result->fetch_assoc()) {
    $data["labels"][] = $row["direccion"];
    $data["values"][] = $row["cantidad"];
}

echo json_encode($data);

$conn->close();
?>
