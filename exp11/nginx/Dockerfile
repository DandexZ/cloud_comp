FROM nginx:alpine

# 安装CGI支持
RUN apk add --no-cache fcgiwrap jq

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.conf.ip-hash /etc/nginx/nginx.conf.ip-hash
COPY nginx.conf.random /etc/nginx/nginx.conf.random
COPY nginx.conf.round-robin /etc/nginx/nginx.conf.round-robin
COPY nginx.conf.weighted /etc/nginx/nginx.conf.weighted
COPY html/ /usr/share/nginx/html/