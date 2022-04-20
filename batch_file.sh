#!/bin/sh
cd "./"
# git checkout dev
python batch_file.py
git add .
git commit -m "made changes"
git push heroku main
echo Press Enter...
read