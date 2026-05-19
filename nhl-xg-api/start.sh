cat > nhl-xg-api/start.sh << 'EOF'
#!/bin/bash
echo "Architecture: $(uname -m)"
echo "Alloy path: $(which alloy 2>/dev/null || echo 'not found')"
ls /usr/local/bin/ | grep alloy || echo "No alloy in /usr/local/bin"
alloy run alloy-config.alloy &
uvicorn app.main:app --host 0.0.0.0 --port $PORT
EOF

chmod +x nhl-xg-api/start.sh