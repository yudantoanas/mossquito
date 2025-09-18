#!/bin/sh
rm -rf $1/extracted

# run main script
python main.py $1

# run MOSS script
./moss.pl -l python -c "MOSS Results" $1/extracted/*.py