#!/bin/bash
# Preview the documentation site locally

echo "🚀 Starting documentation server..."
echo ""
echo "📖 Documentation site: http://localhost:8000"
echo "⌨️  Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
python3 -m http.server 8000
