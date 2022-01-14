#!/usr/bin/env bash

# abort on errors
set -e

npm run build

cd dist

git add -A
git commit -m 'deploy'

git push -f git@github.com:fabianallendorf/klixx-web.git main:gh-pages

cd -