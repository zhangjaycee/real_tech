#!/bin/bash

git pull
./detect.py
./wordcloud.py
git add .
git commit -m "touch empty files"
git push
