#!/bin/bash
pipenv lock -r > requirements.txt
pipenv lock -r -d >> requirements.txt
sort requirements.txt | uniq > merged_requirements.txt
mv merged_requirements.txt requirements.txt
git add requirements.txt
