<?php


function file_get_contents_curl($url) {
    // use cURL to fetch instead of file_get_contents. more extensible
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_HEADER, 0);
    //curl_setopt($ch, CURLOPT_COOKIEJAR, './cookiejar.txt'); // put cookie in jar?
    //curl_setopt($ch, CURLOPT_COOKIEFILE, './cookiejar.txt');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); //Set curl to return data
    curl_setopt($ch, CURLOPT_URL, $url);

    $data = curl_exec($ch);
    curl_close($ch);

    return $data;
}


$url = $_GET['url'];
// for debugging
//$url = "http://alexmoye.pbworks.com/api_v2/op/GetPageRevisions/page/Ben+Smith+Day+1/_type/jsontext";
$url = str_replace(' ', '+', $url);
header('Content-type: application/json');

// rid ourselves of needless header response
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


// reply with the json result
echo $return . "\n";


?>
