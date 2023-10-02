#!/bin/bash

# Publish Script
# 1. Clones website-v7 repo
# 2. Writes blog content to file
# 3. Downloads images
# 4. Commits changes to staging branch
# 5. Builds website
# 6. Clone github website repo
# 7. Copies assets to website repo
# 8. Commits and publishes changes to website repo
# 9. Kickback and relax

# Reaffirm GO path
export PATH=/usr/local/go/bin:$PATH

echo "Cloning ${GITHUB_REPOSITORY} repo..."

# Weird hack for jinja2 template rendering, that strips out newlines
PARSED_BLOG_CONTENT="${BLOG_CONTENT//<NEW_LINE_TOKEN>/\\n}"

mkdir -p /tmp/gh
cd /tmp/gh || exit 127
rm -rf website-v7
git clone "$CLONE_URL"
cd website-v7 || exit 127
git checkout master
cd content/post || exit 127

echo "Writing to file..."

touch "$BLOG_FILENAME"
echo "$PARSED_BLOG_CONTENT" > "$BLOG_FILENAME"

# Replace \n with actual newlines
awk '{gsub(/\\n/,"\n")}1' "$BLOG_FILENAME" > "$BLOG_FILENAME.tmp" && mv "$BLOG_FILENAME.tmp" "$BLOG_FILENAME"
rm "$BLOG_FILENAME.tmp"
ls -lart
cat "$BLOG_FILENAME"

echo "Downloading images..."
IMAGE_DIR=/tmp/gh/website-v7/static/images/hero
declare -a IMAGE_URLS=("$PREVIEW_URL" "$DESKTOP_URL" "$TABLET_URL" "$MOBILE_URL" "$FALLBACK_URL")
declare -a IMAGE_LOCATIONS=("$IMAGE_DIR"/"$BLOG_TITLE".preview.jpg "$IMAGE_DIR"/"$BLOG_TITLE".desktop.jpg "$IMAGE_DIR"/"$BLOG_TITLE".tablet.jpg "$IMAGE_DIR"/"$BLOG_TITLE".mobile.jpg "$IMAGE_DIR"/"$BLOG_TITLE".fallback.jpg)
IMAGE_SIZE=5

for (( i=0; i<IMAGE_SIZE; i++ ));
do
  echo "Downloading: ${IMAGE_URLS[$i]}"
  curl -o "${IMAGE_LOCATIONS[$i]}" "${IMAGE_URLS[$i]}"
done

echo "Committing changes..."

git config user.email "mohseenmukaddam6@gmail.com"
git config user.name "mohseenrm"

cd /tmp/gh/website-v7 || exit 127

git add .
git commit -m "Adding new blog post"
git push origin master

echo "Done! $BLOG_FILENAME published to staging."

cd /tmp/gh || exit 127

echo "Cloning ${GITHUB_WEBSITE_REPOSITORY} repo..."

rm -rf mohseenrm.github.io
git clone "$CLONE_WEBSITE_REPO_URL"

echo "Cleaning up old assets..."
cd mohseenrm.github.io || exit 127
rm -rf about css authors fonts page js images scss post
rm index.xml index.html sitemap.xml

echo "Building website..."
cd /tmp/gh/website-v7 || exit 127
hugo --gc --minify --destination /tmp/gh/mohseenrm.github.io

echo "Copying assets..."
cp -r /tmp/gh/mohseenrm.github.io/public/* /tmp/gh/mohseenrm.github.io
rm -rf /tmp/gh/mohseenrm.github.io/public

echo "Committing changes..."
cd /tmp/gh/mohseenrm.github.io || exit 127
git add .

git config user.email "mohseenmukaddam6@gmail.com"
git config user.name "mohseenrm"

git commit -m "Publishing new blog post"
git push origin master
