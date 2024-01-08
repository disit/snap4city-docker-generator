<?php
$output = false;

$key = hash('sha256', '$#aes-encryption-key-16chars#$');

$iv = substr(hash('sha256', '$#aes-encryption-iv-16chars#$'), 0, 16);

$output = openssl_encrypt('$#virtuoso-kb-pwd#$', 'AES-256-CBC', $key, 0, $iv);

$output = base64_encode($output);

echo $output;
?>
