#!/usr/bin/env python3

# version 4

# USAGE:
# python3 assembler.py [--run] [input_file]

import importlib
import sys
from bytecode import Bytecode, Compare, Instr, Label 

# process command line arguments

run = False

if len(sys.argv) > 1:
    if '--run' in sys.argv:
        run = True
        sys.argv.remove('--run')
       
if len(sys.argv) > 1:
    sys.stdin = open(sys.argv[1], 'r', encoding='utf-8')

# bytecode assembling

comps = {'==': Compare.EQ, '!=': Compare.NE,
          '<': Compare.LT, '<=': Compare.LE,
          '>': Compare.GT, '>=': Compare.GE}
instructions = []
labels = {}
lineno = 0

for line in sys.stdin:
    # line cleanup
    line = line.strip()
    lineno += 1
    if line == '' or line.startswith('#'):
        continue
        
    op = line.split()
    if len(op) == 1:
        # single opcode
        if op[0].endswith(':'):
            # handle label definition
            label = op[0][:-1]
            if label not in labels:
                labels[label] = Label()
            instructions.append(labels[label])
        else:
            # normal opcode
            instructions.append(Instr(op[0]))
    else:
        # opcode and parameter
        if op[1].isdigit():
            instructions.append(Instr(op[0], int(op[1])))
        else:
            # cleanup parameter
            s = op[1].replace('"', '').replace('\\n', '\n').rstrip()
            if op[0] == 'COMPARE_OP':
                if s not in comps:
                    print(f"unknown comparison operator '{s}' in line {lineno}", file=sys.stderr)
                    sys.exit(1)
                instructions.append(Instr(op[0], comps[s]))
            elif op[0] == 'POP_JUMP_IF_FALSE' or op[0] == 'JUMP_ABSOLUTE':
                # handle label usage
                label = op[1]
                if label not in labels:
                    labels[label] = Label()
                instructions.append(Instr(op[0], labels[label]))
            else:
                # normal opcode
                instructions.append(Instr(op[0], s))

bytecode = Bytecode(instructions)
code = bytecode.to_code()

# export bytecode to a executable pyc file 

pyc_data = importlib._bootstrap_external._code_to_timestamp_pyc(code)
pyc = open('program.pyc', 'wb')
pyc.write(pyc_data)
pyc.close()

# directly execute bytecode

if run:
    exec(code)

