#!/bin/sh

# 启动 fcgiwrap
echo "🔧 Starting fcgiwrap..."
spawn-fcgi -s /var/run/fcgiwrap.socket -U nginx -u nginx -n /usr/bin/fcgiwrap &
echo "nginx ALL=(root) NOPASSWD: /usr/sbin/nginx -s reload" >> /etc/sudoers



# 启动 nginx
echo "🚀 Starting nginx..."
nginx -g "daemon off;"
