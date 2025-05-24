#!/bin/sh

echo "Content-Type: application/json"
echo ""

# Read input
read -n $CONTENT_LENGTH POST_DATA

# Parse strategy
strategy=$(echo $POST_DATA | jq -r '.strategy')

# Update nginx.conf based on strategy
case $strategy in
    "round-robin")
        cat /etc/nginx/nginx.conf.round-robin > /etc/nginx/nginx.conf
        ;;
    "random")
        cat /etc/nginx/nginx.conf.random > /etc/nginx/nginx.conf
        ;;
    "weighted")
        cat /etc/nginx/nginx.conf.weighted > /etc/nginx/nginx.conf
        ;;
    "ip-hash")
        cat /etc/nginx/nginx.conf.ip-hash > /etc/nginx/nginx.conf
        ;;
    *)
        echo '{"status": "error", "message": "Invalid strategy"}'
        exit 1
        ;;
esac

# Reload nginx
RELOAD_OUTPUT=$(sudo /usr/sbin/nginx -s reload 2>&1)
RELOAD_STATUS=$?
if [ $RELOAD_STATUS -ne 0 ]; then
    USERIS=$(whoami)
    echo '{"status": "error","user": "'$USERIS'", "message": "Failed to reload nginx: '$RELOAD_OUTPUT'"}'
    exit 1
fi

echo '{"status": "success", "strategy": "'$strategy'", "message": "Strategy updated successfully"}'