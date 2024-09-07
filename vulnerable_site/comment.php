<?php
// Vulnerable PHP code for XSS (example)
if (isset($_POST['comment'])) {
    $comment = $_POST['comment'];
    echo "User comment: " . $comment;  // Reflecting user input directly without sanitization
}
?>
