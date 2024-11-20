
<?php
session_start();
if (!isset($_SESSION['user'])) {
    header("Location: login.html");
    exit;
}

$conn = new mysqli("localhost", "root", "", "sonometro_iot");

if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

$sql = "SELECT * FROM registro";
$result = $conn->query($sql);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <h2>Dashboard</h2>
    <table border="1">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nivel 1</th>
                <th>Nivel 2</th>
                <th>Nivel 3</th>
                <th>Fecha</th>
                <th>Excede Limite</th>
            </tr>
        </thead>
        <tbody>
            <?php while ($row = $result->fetch_assoc()): ?>
            <tr>
                <td><?php echo $row['idRegistro']; ?></td>
                <td><?php echo $row['nivelSonido1']; ?></td>
                <td><?php echo $row['nivelSonido2']; ?></td>
                <td><?php echo $row['nivelSonido3']; ?></td>
                <td><?php echo $row['fechaRegistro']; ?></td>
                <td><?php echo $row['excedeLimite'] ? 'Sí' : 'No'; ?></td>
            </tr>
            <?php endwhile; ?>
        </tbody>
    </table>
</body>
</html>
<?php $conn->close(); ?>
