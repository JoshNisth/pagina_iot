<?php
$conn = new mysqli("localhost", "root", "", "sonometro_iot");

if ($conn->connect_error) {
    die(json_encode(["error" => "Error de conexión a la base de datos."]));
}

$action = $_GET['action'];
$filters = json_decode($_GET['filters'], true);

// Construcción de filtros dinámicos
$whereClauses = [];

if (!empty($filters['profile'])) {
    $whereClauses[] = "u.tipo_idTipo = " . (int)$filters['profile'];
}

if (!empty($filters['user'])) {
    $whereClauses[] = "u.idUsuario = " . (int)$filters['user'];
}

if (!empty($filters['date'])) {
    $whereClauses[] = "DATE(r.fechaRegistro) = '" . $conn->real_escape_string($filters['date']) . "'";
}

$whereSQL = count($whereClauses) > 0 ? "WHERE " . implode(" AND ", $whereClauses) : "";

// Procesar la acción solicitada
if ($action === "getUserChart") {
    $query = "
        SELECT u.nombreUsuario AS label, COUNT(r.idRegistro) AS value
        FROM usuario u
        INNER JOIN registro r ON u.idUsuario = r.usuario_idUsuario
        $whereSQL
        GROUP BY u.idUsuario
    ";
} elseif ($action === "getProfileExcessChart") {
    $query = "
        SELECT t.nombreTipo AS label, COUNT(r.idRegistro) AS value
        FROM registro r
        INNER JOIN usuario u ON r.usuario_idUsuario = u.idUsuario
        INNER JOIN tipo t ON u.tipo_idTipo = t.idTipo
        WHERE r.excedeLimite = 1
        " . ($whereSQL ? " AND " . substr($whereSQL, 6) : "") . "
        GROUP BY t.idTipo
    ";
} elseif ($action === "getProfileChart") {
    $query = "
        SELECT t.nombreTipo AS label, COUNT(r.idRegistro) AS value
        FROM tipo t
        INNER JOIN usuario u ON t.idTipo = u.tipo_idTipo
        INNER JOIN registro r ON u.idUsuario = r.usuario_idUsuario
        $whereSQL
        GROUP BY t.idTipo
    ";
} else {
    die(json_encode(["error" => "Acción no válida."]));
}

// Ejecutar consulta y devolver resultados
$result = $conn->query($query);
$data = ["labels" => [], "values" => []];
while ($row = $result->fetch_assoc()) {
    $data["labels"][] = $row["label"];
    $data["values"][] = $row["value"];
}

echo json_encode($data);

$conn->close();
?>
