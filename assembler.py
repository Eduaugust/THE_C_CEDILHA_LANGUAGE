#!/usr/bin/env python3

# version 5

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
f_instructions = []
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
        elif op[0] == '.end':
            # end function declaration
            bytecode.extend(instructions)
            instructions = []
            code = bytecode.to_code()
            # create variable for function 
            f_instructions.extend([Instr("LOAD_CONST", code),
                                   Instr("LOAD_CONST", function_name),
                                   Instr("MAKE_FUNCTION", 0),
                                   Instr("STORE_NAME", function_name)])
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
            elif op[0] == '.begin':
                # begin function declaration
                function_name = op[1] # save function name 
                bytecode = Bytecode()
                bytecode.argnames = op[2:] # list of named arguments
                bytecode.argcount = len(op[2:])
            else:
                # normal opcode
                instructions.append(Instr(op[0], s))

bytecode = Bytecode(f_instructions + instructions)
code = bytecode.to_code()

# export bytecode to a executable pyc file 

pyc_data = importlib._bootstrap_external._code_to_timestamp_pyc(code)
pyc = open('program.pyc', 'wb')
pyc.write(pyc_data)
pyc.close()

# directly execute bytecode

if run:
    exec(code)

