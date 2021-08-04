server {
    server_name 

    listen 80;

    gzip on;
    gzip_comp_level 4;
    gzip_types text/html text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
    client_max_body_size 20M;
    access_log    /var/log/nginx/access.log;

    location / {
        proxy_pass            http://docker;  
        proxy_http_version    1.1;

        proxy_set_header      Connection      $connection_upgrade;
        proxy_set_header      Upgrade         $http_upgrade;
        proxy_set_header      Host            $host;
        proxy_set_header      X-Real-IP       $remote_addr;
        proxy_set_header      X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    if ($http_x_forwarded_proto = 'http') {
        return 301 https://$host$request_uri;
    }
}