#!/bin/bash

# Set your PGP key ID
PGP_KEY_ID="10E75F565D2CD2D3"

# Set the folders where your markdown files and signed files will be located
TARGET_FOLDER="./content"
STATIC_FOLDER="./static"

# Export GPG environment variables
export GNUPGHOME="/home/lupos/.gnupg"
GPG_TTY=$(tty)
export GPG_TTY

# Check if a commit message is provided as an argument
if [ -n "$1" ]; then
    COMMIT_MESSAGE="$1"
else
    echo "Error: Please provide a commit message."
    exit 1
fi

# Find all markdown files recursively and sign each with the PGP key
find "$TARGET_FOLDER" -type f \( -name "*.md" -o -name "*.html" \) -exec sh -c '
    for file do
        gpg --yes --armor --output "$file.asc" --detach-sign --default-key "$PGP_KEY_ID" "$file"
    done
' sh {} +

# Find all .asc files in the source folder and move them to the static folder
find "$TARGET_FOLDER" -type f -name "*.asc" -exec mv {} "$STATIC_FOLDER" \;

# Add all changes to Git
git add "$TARGET_FOLDER"/*.asc

# Commit changes
git commit -S -m "$COMMIT_MESSAGE"

# Push changes to remote repository
git push
