<?php
// Vulnerable PHP code (example)
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "test_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Unsanitized input (SQL Injection Vulnerability)
$query = $_GET['query'];
$sql = "SELECT * FROM users WHERE name = '$query'";

$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "<table>";
    while ($row = $result->fetch_assoc()) {
        echo "<tr><td>" . $row["id"] . "</td><td>" . $row["name"] . "</td></tr>";
    }
    echo "</table>";
} else {
    echo "0 results";
}

$conn->close();
?>
