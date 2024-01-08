ANON=$(docker-compose exec dashboard-builder php /var/www/html/dashboardSmartCity/conf/ssl_expose.php)
echo the new anonymous hash is $ANON
