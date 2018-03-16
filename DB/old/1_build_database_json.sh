#!/bin/bash
echo "Json Databse will be built based on all files located in Data/.
Final file is db_imsi located in db/. Core treatments in db/import_raw.py."
find ../db:/ -name "out.txt" -exec cat {} \;|python import_raw.py
