<?php
session_start();
$message = '';

if (isset($_POST["submit"])) {
    $fileName = $_FILES["uploadedFile"]["name"];
    $fileTmpName = $_FILES["uploadedFile"]["tmp_name"];
    $fileError = $_FILES["uploadedFile"]["error"];
    $uploadDirectory = "uploads/";
    
    // ========== ПРОВЕРКА ПО РАСШИРЕНИЮ ==========
    
    # Разрешенные расширения (только строчные буквы)
    $allowedExtensions = ['pdf', 'jpg', 'jpeg', 'png', 'gif'];

    // 1. Получаем расширение файла в нижнем регистре
    $fileExtension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));
    
    // 2. Проверяем, есть ли расширение вообще
    if (empty($fileExtension)) {
        $message = "Ошибка: Файл не имеет расширения.";
    }
    // 3. Проверка расширения
    elseif (!in_array($fileExtension, $allowedExtensions)) {
        $message = "Ошибка: Разрешены только файлы PDF, JPG, PNG, GIF.";
    }
    // 4. Проверяем ошибки загрузки
    elseif ($fileError !== 0) {
        $message = "Ошибка загрузки файла. Код ошибки: $fileError";
    }
    // 5. Всё ок - загружаем
    else {
        // ⚠️ ВАЖНО: Генерируем УНИКАЛЬНОЕ имя, а не используем оригинальное!
        $uniqueFileName = uniqid('file_', true) . '.' . $fileExtension;
        $uploadPath = $uploadDirectory . $uniqueFileName;
        
        if (move_uploaded_file($fileTmpName, $uploadPath)) {
            $message = "Файл успешно загружен! Сохранён как: " . htmlspecialchars($uniqueFileName);
        } else {
            $message = "Ошибка при сохранении файла.";
        }
    }
}
?>