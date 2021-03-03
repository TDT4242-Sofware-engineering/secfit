server {
    server_name  secfit.vassbo.as;

    listen [::]:443 ssl; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/secfit.vassbo.as/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/secfit.vassbo.as/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


    location / {
        proxy_pass http://192.168.0.20:4010;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
    location /api/ {
        proxy_pass http://192.168.0.20:4009;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
    location /api/root/ {
        proxy_pass http://192.168.0.20:4009;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
    location /admin/ {
        proxy_pass http://192.168.0.20:4009;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
    location /static/ {
        proxy_pass http://192.168.0.20:4009;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
    location /media/ {
        proxy_pass http://192.168.0.20:4009;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}

server {
    if ($host = secfit.vassbo.as) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen            80;
    listen       [::]:80;
    server_name  secfit.vassbo.as;
    return 404; # managed by Certbot
}