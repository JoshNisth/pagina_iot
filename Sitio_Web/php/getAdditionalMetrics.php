<?php
$conn = new mysqli("localhost", "root", "", "sonometro_iot");

if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

$action = $_GET['action'];

if ($action === 'getMetrics') {
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

    // Perfil más popular
    $result = $conn->query("
        SELECT t.nombreTipo AS name, COUNT(u.idUsuario) AS total
        FROM tipo t
        INNER JOIN usuario u ON t.idTipo = u.tipo_idTipo
        GROUP BY t.idTipo
        ORDER BY total DESC
        LIMIT 1
    ");
    $mostPopularProfile = $result->fetch_assoc();

    // Cantidad de veces que se excedió el límite
    $result = $conn->query("SELECT COUNT(*) AS maxDbCount FROM registro WHERE excedeLimite = 1");
    $maxDbCount = $result->fetch_assoc()["maxDbCount"];

    // Promedio general de decibelios
    $result = $conn->query("SELECT AVG(nivelSonido1) AS avgDb FROM registro");
    $avgDb = round($result->fetch_assoc()["avgDb"], 2);

    echo json_encode([
        "mostActiveUser" => ["name" => $mostActiveUser["name"], "percentage" => round($mostActiveUser["total"] / 100, 2)],
        "mostPopularProfile" => ["name" => $mostPopularProfile["name"], "percentage" => round($mostPopularProfile["total"] / 100, 2)],
        "maxDbCount" => $maxDbCount,
        "avgDb" => $avgDb
    ]);
}

if ($action === 'getUsersChart') {
    $result = $conn->query("
        SELECT u.nombreUsuario AS label, COUNT(r.idRegistro) AS value
        FROM usuario u
        INNER JOIN registro r ON u.idUsuario = r.usuario_idUsuario
        GROUP BY u.idUsuario
    ");

    $data = ["labels" => [], "values" => []];
    while ($row = $result->fetch_assoc()) {
        $data["labels"][] = $row["label"];
        $data["values"][] = $row["value"];
    }

    echo json_encode($data);
}

if ($action === 'getExceedLimitChart') {
    $result = $conn->query("
        SELECT t.nombreTipo AS label, COUNT(r.idRegistro) AS value
        FROM registro r
        INNER JOIN usuario u ON r.usuario_idUsuario = u.idUsuario
        INNER JOIN tipo t ON u.tipo_idTipo = t.idTipo
        WHERE r.excedeLimite = 1
        GROUP BY t.idTipo
    ");

    $data = ["labels" => [], "values" => []];
    while ($row = $result->fetch_assoc()) {
        $data["labels"][] = $row["label"];
        $data["values"][] = $row["value"];
    }

    echo json_encode($data);
}

$conn->close();
?>
