<?php
function file_get_contents_curl($url) {
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); //Set curl to return data
    curl_setopt($ch, CURLOPT_URL, $url);

    $data = curl_exec($ch);
    curl_close($ch);

    return $data;
}


$url = $_GET['url'];
header('Content-type: application/json');

$response = trim(file_get_contents_curl($url));
$explosion = explode("\n", $response);
$lastindex = count($explosion) - 1;
if($explosion[$lastindex] == '*/'){
    unset($explosion[$lastindex]);
}
if($explosion[0] == '/*-secure-'){
    unset($explosion[0]);
}
$return = implode("\n", $explosion);

echo $return . "\n";


?>
