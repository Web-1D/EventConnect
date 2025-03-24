#!/bin/bash

echo "🚀 Starting cleanup..."

# 1. Remove unwanted files/folders
rm -rf .idea
rm -rf env
rm -f db.sqlite3
rm -f .DS_Store
rm -f requirments.txt

# 2. Add .gitignore if missing
if [ ! -f .gitignore ]; then
    echo "📄 Creating .gitignore"
    cat <<EOL > .gitignore
__pycache__/
*.py[cod]
*.sqlite3
*.log

env/
venv/

.DS_Store

.vscode/
.idea/

db.sqlite3
/static/
media/
EOL
fi

# 3. Git commands
echo "Staging all changes..."
git add .

echo "Committing..."
git commit -m "Cleaned up repo"

echo "Pushing to branch costi..."
git push origin costi

echo "Done!
