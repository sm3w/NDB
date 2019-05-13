#!/bin/sh


(pyinstaller -F --distpath dist --workpath build ../src/main.py)
echo "Copying data files"
(cp -rp ../src/database/ dist)
