#!/usr/bin/env bash
chmod +x compiler.py
chmod +x assembler.py


# Use o primeiro argumento como o nome do arquivo, ou 'simple-print.c' se nenhum argumento foi passado
FILE=${1:-simple-print.c}

./compiler.py $FILE program.pyasm
./assembler.py --run program.pyasm