<?php
$conn = new mysqli("localhost", "root", "", "sonometro_iot");

if ($conn->connect_error) {
    die(json_encode(["error" => "Error de conexión a la base de datos."]));
}

$action = $_GET['action'];

if ($action === "getProfileChart") {
    // Registros por Perfil basados en los registros en la tabla `registro`
    $result = $conn->query("
        SELECT t.nombreTipo AS label, COUNT(r.idRegistro) AS value
        FROM tipo t
        INNER JOIN usuario u ON t.idTipo = u.tipo_idTipo
        INNER JOIN registro r ON u.idUsuario = r.usuario_idUsuario
        GROUP BY t.idTipo
    ");

    $data = ["labels" => [], "values" => []];
    while ($row = $result->fetch_assoc()) {
        $data["labels"][] = $row["label"];
        $data["values"][] = $row["value"];
    }
    echo json_encode($data);
}

if ($action === "getUserChart") {
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

if ($action === "getProfileExcessChart") {
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
