#!/bin/bash
echo "🔨 Building Tailwind CSS..."
docker exec website-web-1 sh -c "cd /app/frontend && npm run build"
echo "📦 Copying CSS to Django static..."
docker exec website-web-1 cp /app/frontend/dist/css/hot_osm_processed.css /app/hot_osm/static/css/hot_osm_processed.css
echo "✅ Done! Hard refresh your browser (Cmd+Shift+R)"
