#!/bin/bash
echo "🔨 Building Tailwind CSS..."
docker exec website-web-1 sh -c "cd /app/frontend && npm run build"
echo "Done! The CSS is built in frontend/dist/css/"
echo "Django will automatically collect it from STATICFILES_DIRS"
echo "Hard refresh your browser (Cmd+Shift+R)"
