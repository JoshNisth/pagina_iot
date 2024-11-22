<?php
$conn = new mysqli("localhost", "root", "", "sonometro_iot");

if ($conn->connect_error) {
    die(json_encode(["error" => "Error de conexión a la base de datos."]));
}

// Total general de registros
$totalRecordsResult = $conn->query("SELECT COUNT(*) AS total FROM registro");
$totalRecords = $totalRecordsResult->fetch_assoc()["total"];

// Usuario más activo
$result = $conn->query("
    SELECT u.nombreUsuario AS name, COUNT(r.idRegistro) AS total
    FROM usuario u
    INNER JOIN registro r ON u.idUsuario = r.usuario_idUsuario
    GROUP BY u.idUsuario
    ORDER BY total DESC
    LIMIT 1
");
$mostActiveUser = $result->fetch_assoc();
$mostActiveUserPercentage = round(($mostActiveUser["total"] / $totalRecords) * 100, 2);

// Perfil más popular (con relación a los registros)
$result = $conn->query("
    SELECT t.nombreTipo AS name, COUNT(r.idRegistro) AS total
    FROM tipo t
    INNER JOIN usuario u ON t.idTipo = u.tipo_idTipo
    INNER JOIN registro r ON u.idUsuario = r.usuario_idUsuario
    GROUP BY t.idTipo
    ORDER BY total DESC
    LIMIT 1
");
$mostPopularProfile = $result->fetch_assoc();
$mostPopularProfilePercentage = round(($mostPopularProfile["total"] / $totalRecords) * 100, 2);

echo json_encode([
    "mostActiveUser" => [
        "name" => $mostActiveUser["name"],
        "percentage" => $mostActiveUserPercentage
    ],
    "mostPopularProfile" => [
        "name" => $mostPopularProfile["name"],
        "percentage" => $mostPopularProfilePercentage
    ]
]);

$conn->close();
?>
