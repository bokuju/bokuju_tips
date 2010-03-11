#!/usr/bin/php
<?php
include '.test_conf';

$request =  'http://api.ustream.tv';
$format = 'php';   // this can be xml, json, html, or php
$method = 'user/recent/search/username:like:bokuju';
//$method = 'stream/all/getMostViewers';
//$method = 'channel/api-test-show/getEmbedTag';
$args = "key=" . $key;

// Get and config the curl session object
$session = curl_init($request.'/'.$format.'/'.$method.'?'.$args);
curl_setopt($session, CURLOPT_HEADER, false);
curl_setopt($session, CURLOPT_RETURNTRANSFER, true);

//execute the request and close
$response = curl_exec($session);
curl_close($session);

// this line works because we requested $format='php' and not some other output format
$resultsArray = unserialize($response);

// this is your data returned; you could do something more useful here than just echo it
var_dump($resultsArray['results']);
?>
