#!/bin/bash

git pull
./detect.py
./generate_wordcloud.py
git add .
git commit -m "touch empty files"
git push
