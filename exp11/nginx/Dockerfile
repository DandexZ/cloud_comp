FROM nginx:alpine

# 安装CGI支持
RUN apk add --no-cache fcgiwrap spawn-fcgi jq sudo

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.conf.ip-hash /etc/nginx/nginx.conf.ip-hash
COPY nginx.conf.random /etc/nginx/nginx.conf.random
COPY nginx.conf.round-robin /etc/nginx/nginx.conf.round-robin
COPY nginx.conf.weighted /etc/nginx/nginx.conf.weighted
COPY html/ /usr/share/nginx/html/
COPY entrypoint.sh /usr/share/nginx/entrypoint.sh

# 启动脚本：同时启动 fcgiwrap 和 nginx
RUN chmod +x /usr/share/nginx/entrypoint.sh
RUN chmod +x /usr/share/nginx/html/change-strategy/change-strategy.sh
RUN chmod +rwx /etc/nginx/nginx.conf

RUN chown nginx:nginx /etc/nginx/nginx.conf
RUN chown nginx:nginx /etc/nginx/nginx.conf.ip-hash
RUN chown nginx:nginx /etc/nginx/nginx.conf.random
RUN chown nginx:nginx /etc/nginx/nginx.conf.round-robin
RUN chown nginx:nginx /etc/nginx/nginx.conf.weighted

CMD ["/usr/share/nginx/entrypoint.sh"]
