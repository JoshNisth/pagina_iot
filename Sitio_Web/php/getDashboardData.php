<?php
$conn = new mysqli("localhost", "root", "", "sonometro_iot");

if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

$action = $_GET['action'];

if ($action === 'getDistribution') {
    $profile = $_GET['profile'];
    $startDate = $_GET['startDate'];
    $endDate = $_GET['endDate'];

    $query = "SELECT d.tipoDir AS label, COUNT(r.idRegistro) AS value
              FROM registro r
              INNER JOIN direcion d ON r.direcion_idDir = d.idDir";

    if ($profile || $startDate || $endDate) {
        $query .= " WHERE 1=1";
        if ($profile) $query .= " AND r.usuario_idUsuario = $profile";
        if ($startDate) $query .= " AND r.fechaRegistro >= '$startDate'";
        if ($endDate) $query .= " AND r.fechaRegistro <= '$endDate'";
    }

    $query .= " GROUP BY d.tipoDir";
    $result = $conn->query($query);

    $data = ["labels" => [], "values" => []];
    while ($row = $result->fetch_assoc()) {
        $data["labels"][] = $row["label"];
        $data["values"][] = $row["value"];
    }

    echo json_encode($data);
}

if ($action === 'getTotalRecordsByDay') {
    $profile = $_GET['profile'];
    $startDate = $_GET['startDate'];
    $endDate = $_GET['endDate'];

    $query = "SELECT DATE(r.fechaRegistro) AS label, COUNT(r.idRegistro) AS value
              FROM registro r";

    if ($profile || $startDate || $endDate) {
        $query .= " WHERE 1=1";
        if ($profile) $query .= " AND r.usuario_idUsuario = $profile";
        if ($startDate) $query .= " AND r.fechaRegistro >= '$startDate'";
        if ($endDate) $query .= " AND r.fechaRegistro <= '$endDate'";
    }

    $query .= " GROUP BY DATE(r.fechaRegistro)";
    $result = $conn->query($query);

    $data = ["labels" => [], "values" => []];
    while ($row = $result->fetch_assoc()) {
        $data["labels"][] = $row["label"];
        $data["values"][] = $row["value"];
    }

    echo json_encode($data);
}

$conn->close();
?>
