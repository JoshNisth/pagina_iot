<?php
$servername = "localhost";
$username = "root";           // Cambia esto por tu usuario de MySQL
$password = "";               // Cambia esto por tu contraseña de MySQL
$dbname = "sonometro_IOT";     // Nombre de la base de datos
try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);

    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $json = file_get_contents('php://input');
    $data = json_decode($json, true);

    if (isset($data['nivelSonido1'], $data['nivelSonido2'], $data['nivelSonido3'], $data['fechaRegistro'], 
              $data['excedeLimite'], $data['direcion_idDir'], $data['usuario_idUsuario'])) {
        

                $usuario_idUsuario = $data['usuario_idUsuario'];
                $stmtLimit = $conn->prepare("SELECT limiteMax FROM tipo 
                                               JOIN usuario ON tipo.idTipo = usuario.tipo_idTipo 
                                               WHERE usuario.idUsuario = :usuario_idUsuario");
                $stmtLimit->bindParam(':usuario_idUsuario', $usuario_idUsuario);
                $stmtLimit->execute();
                
                $resultado = $stmtLimit->fetch(PDO::FETCH_ASSOC);
                $limiteMax = $resultado['limiteMax'];
        
                // Determinar si el nivel de sonido excede el límite
                $excedeLimite = ($data['nivelSonido1'] > $limiteMax) ? true : false;
                
        $stmt = $conn->prepare("INSERT INTO registro (nivelSonido1, nivelSonido2, nivelSonido3, fechaRegistro, excedeLimite, 
                               direcion_idDir, usuario_idUsuario)
                                VALUES (:nivelSonido1, :nivelSonido2, :nivelSonido3, :fechaRegistro, :excedeLimite, 
                                        :direcion_idDir, :usuario_idUsuario)");

        $stmt->bindParam(':nivelSonido1', $data['nivelSonido1']);
        $stmt->bindParam(':nivelSonido2', $data['nivelSonido2']);
        $stmt->bindParam(':nivelSonido3', $data['nivelSonido3']);
        $stmt->bindParam(':fechaRegistro', $data['fechaRegistro']);
        $stmt->bindParam(':excedeLimite', $data['excedeLimite'], PDO::PARAM_BOOL); // Aseguramos que sea un booleano
        $stmt->bindParam(':direcion_idDir', $data['direcion_idDir']);
        $stmt->bindParam(':usuario_idUsuario', $data['usuario_idUsuario']);

        if ($stmt->execute()) {
            echo json_encode(["message" => "Datos insertados exitosamente"]);
        } else {
            echo json_encode(["message" => "nivelSonido2 al insertar los datos"]);
        }
    } else {
        echo json_encode(["message" => "Datos incompletos en Del JSON recibido"]);
    }
} catch (PDOException $e) {
    echo json_encode(["nivelSonido2" => "nivelSonido2 en la conexión: " . $e->getMessage()]);
}
$conn = null;
?>