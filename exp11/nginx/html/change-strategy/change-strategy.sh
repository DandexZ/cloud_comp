#!/bin/bash

echo "Content-Type: application/json"
echo ""

# Read input
read -n $CONTENT_LENGTH POST_DATA

# Parse strategy
strategy=$(echo $POST_DATA | jq -r '.strategy')

# Update nginx.conf based on strategy
case $strategy in
    "round-robin")
        cp /etc/nginx/nginx.conf.round-robin /etc/nginx/nginx.conf
        ;;
    "random")
        cp /etc/nginx/nginx.conf.random /etc/nginx/nginx.conf
        ;;
    "weighted")
        cp /etc/nginx/nginx.conf.weighted /etc/nginx/nginx.conf
        ;;
    "ip-hash")
        cp /etc/nginx/nginx.conf.ip-hash /etc/nginx/nginx.conf
        ;;
    *)
        echo '{"status": "error", "message": "Invalid strategy"}'
        exit 1
        ;;
esac

# Reload nginx
nginx -s reload 2>/dev/null

echo '{"status": "success", "strategy": "'$strategy'", "message": "Strategy updated successfully"}'