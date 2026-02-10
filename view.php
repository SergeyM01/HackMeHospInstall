<?php
session_start(); 
$message = '';

// Проверяем, авторизован ли пользователь
if (!isset($_SESSION['patient_id'])) {
    die("Access denied. Please login first.");
}

if (isset($_GET['patient_id'])) { 
    $requestedPatientId = $_GET['patient_id']; 
    
    // ВАЖНО: Проверяем, совпадает ли запрошенный ID с ID текущего пользователя
    // Это предотвращает просмотр чужих записей
    if ($requestedPatientId != $_SESSION['patient_id']) {
        die("Access denied. You can only view your own records.");
    }
    
    $patientId = $requestedPatientId; // Теперь безопасно использовать

    $conn = new mysqli("localhost", "root", "", "hackme");
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Используем подготовленные запросы для предотвращения SQL-инъекций
    $sql = "SELECT * FROM patient_records WHERE patient_id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $patientId);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $message = "<table><tr><th>Record Date</th><th>Diagnosis</th><th>Treatment</th><th>Notes</th></tr>";
        while($record = $result->fetch_assoc()) {
            $message .= "<tr><td>" . htmlspecialchars($record['record_date']) . "</td>";
            $message .= "<td>" . htmlspecialchars($record['diagnosis']) . "</td>";
            $message .= "<td>" . htmlspecialchars($record['treatment']) . "</td>";
            $message .= "<td>" . htmlspecialchars($record['notes']) . "</td></tr>";
        }
        $message .= "</table>";
    } else {
        $message = "No records found for this patient.";
    }

    $stmt->close();
    $conn->close();

} else {
    $message = "No patient ID provided.";
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>View Patient Records</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-image: url('your-background-image.jpg');
            background-size: cover;
            background-position: center;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: rgba(255, 255, 255, 0.9);
        }
        th, td {
            padding: 8px;
            text-align: center; 
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        .container {
            text-align: center;
            padding: 20px;
        }
        .button {
            display: inline-block;
            padding: 10px 10px;
            margin: 50px;
            font-size: 16px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            outline: none;
            color: #fff;
            background-color: #4CAF50;
            border: none;
            border-radius: 15px;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>View Patient Records</h1>
        <div class="info"><?php echo $message; ?></div>
        <a href="loginpage.php" class="button">Back to Main Page</a>
        <a href="book_appointment.php" class="button">Book an Appointment</a>
        <a href="order_medication.php" class="button">Order Prescription Medication</a>
        <a href="account_settings.php?id=<?php echo $_SESSION['patient_id']; ?>" class="button">Account Settings</a>
    </div>
</body>
</html>