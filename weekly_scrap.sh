#!/bin/bash

python3 scraper.py
python3 format.py
python3 gsheet.py
echo "gsheet has been updated"