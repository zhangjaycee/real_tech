#!/bin/bash

git pull
./detect.py
git add .
git commit -m "touch empty files"
git push
