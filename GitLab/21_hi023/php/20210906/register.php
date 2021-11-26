<?php
    $con = mysqli_connect("localhost", "root", "haniumhi_023", "testdb");
    mysqli_query($con,'SET NAMES utf8');

    $userID = $_POST["userID"];
    $userPassword = $_POST["userPassword"];
    $userEmail = $_POST["userEmail"];


    $statement = mysqli_prepare($con, "INSERT INTO user VALUES (?,?,?)");
    mysqli_stmt_bind_param($statement, "sssi", $userID, $userPassword, $userEmail);
    mysqli_stmt_execute($statement);


    $response = array();
    $response["success"] = true;


    echo json_encode($response);

?>