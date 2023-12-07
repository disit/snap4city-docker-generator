<?php
$output = false;

$key = hash('sha256', 'EncryptionIniKey');

$iv = substr(hash('sha256', 'IVKeyivKey123456'), 0, 16);

$output = openssl_encrypt('92NfA0wTMg9RU8V7', 'AES-256-CBC', $key, 0, $iv);

$output = base64_encode($output);

echo $output;
?>
