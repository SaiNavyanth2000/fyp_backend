#!/bin/sh
cd "./"
# git checkout dev
git add .
git commit -m "made changes"
git push heroku main
echo Press Enter...
read