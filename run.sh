#!/bin/sh
rm -rf moss

mkdir moss

# run main script
python app.py $1

# run MOSS script
./moss.pl -l python -c "MOSS Results" ./moss/*.py