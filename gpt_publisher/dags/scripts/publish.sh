#!/bin/bash

echo "Cloning website-v7 repo..."

# Weird hack for jinja2 template rendering, that strips out newlines
PARSED_BLOG_CONTENT="${BLOG_CONTENT//<NEW_LINE_TOKEN>/\\n}"

mkdir -p /tmp/gh
cd /tmp/gh || exit 127
rm -rf website-v7
git clone "$CLONE_URL"
cd website-v7 || exit 127
git checkout staging
cd content/post || exit 127

echo "Writing to file..."

touch "$BLOG_FILENAME"
echo "$PARSED_BLOG_CONTENT" > "$BLOG_FILENAME"

# Replace \n with actual newlines
awk '{gsub(/\\n/,"\n")}1' "$BLOG_FILENAME" > "$BLOG_FILENAME.tmp" && mv "$BLOG_FILENAME.tmp" "$BLOG_FILENAME"
rm "$BLOG_FILENAME.tmp"
ls -lart
cat "$BLOG_FILENAME"

echo "Committing changes..."

git config user.email "mohseenmukaddam6@gmail.com"
git config user.name "mohseenrm"

git add .
git commit -m "Adding new blog post"
git push origin staging

echo "Done! $BLOG_FILENAME published to staging."