#!/usr/bin/env python3

# USAGE:
# python3 compiler.py [input_file [output_file]]

import sys
from sly import Lexer, Parser

#################### LEXER ####################

class ÇLexer(Lexer):
    
    # token definitions
    literals = {';', '+', '-', '*', '/', '(', ')', '{', '}', ',', '=', '%', '[', ']'}
    tokens = {STDIO, INT, MAIN, PRINTF, STRING, NUMBER, NAME, IF, COMP, WHILE, BREAKCONTINUE, VOID, RETURN}
    STDIO   = '#include <stdio.h>'
    INT     = 'int'
    MAIN    = 'main'
    PRINTF  = 'printf'
    STRING  = r'"[^"]*"'
    NUMBER  = r'\d+'
    IF  = 'if'
    COMP = r'(==|!=|<=|>=|<|>)'
    WHILE = 'while'
    BREAKCONTINUE = r'(break|continue)'
    VOID = 'void'
    RETURN = 'return'

    # Deixar por último para não conflitar com as palavras reservadas
    NAME    = r'[a-z]+'

    # ignored characters and patterns
    ignore = r' \t'
    ignore_newline = r'\n+'
    ignore_comment = r'//[^\n]*'

    # extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # error handling method
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' in line {self.lineno}")
        self.index += 1

#################### PARSER ####################

class ÇParser(Parser):
    tokens = ÇLexer.tokens

    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'

    def __init__(self):
        self.symbols_table = []
        self.used_vars = []

        # if statements
        self.if_count = 1
        self.if_labels = []

        # while statements
        self.while_count = 1
        self.while_labels = []

        # array
        self.num_elements = 0

        # parameter
        self.parameter_symbol_table = []

    # error handling method
    def show_error(self, mesg, line=None):
        if line:
            mesg += f' in line {line}'

        print(f'{self.RED}error:', mesg, self.END, file=sys.stderr)
        sys.exit(1)
    
    def show_warning(self, mesg, line=None):
        if line:
            mesg += f' in line {line}'

        print(f'{self.YELLOW}warning:', mesg, self.END, file=sys.stderr)
    
    # ---------------- program ----------------

    @_('stdio functions')
    def program(self, p):
        print('\n# symbols table:', self.symbols_table)
        print('\n# used variables:', self.used_vars)
        unusued_vars = [var for var, used in zip(self.symbols_table, self.used_vars) if not used]
        if unusued_vars:
            for var in unusued_vars:
                self.show_warning(f'{var} is defined but never used')

    @_('STDIO')
    def stdio(self, p):
        print("# include <stdio.h>")
        print('LOAD_CONST 0')
        print('LOAD_CONST None')
        print('IMPORT_NAME runtime')
        print('IMPORT_STAR')
        print()

    # ---------------- functions --------------

    @_('function functions')
    def functions(self, p):
        pass

    @_('main')
    def functions(self, p):
        pass

    @_('NAME "(" parameters ")"' )
    def function_name(self,p):
        print("# void", p.NAME, "(){}")
        print('.begin', p.NAME, p.parameters)
        # Adicionar nome dos parametros na tabela de simbolos
        for param in p.parameters.split():
            self.symbols_table.append(param)
            self.used_vars.append(False)
            print("# param", param)
        print()

    @_('VOID function_name "{" statements "}"')
    def function(self, p):
        print('LOAD_CONST None')
        print('RETURN_VALUE')
        print('.end ')
        print('# symbols table:', self.symbols_table)
        print('# used variables:', self.used_vars)
        self.symbols_table = []
        self.used_vars = []
        print()
    
    @_('INT function_name "{" statements "}"')
    def function(self, p):
        print('.end ')
        print('# symbols table:', self.symbols_table)
        print('# used variables:', self.used_vars)
        self.symbols_table = []
        self.used_vars = []
        print()
    
    @_('RETURN expression ";"')
    def return_st(self, p):
        print('RETURN_VALUE')

    # ---------------- parameters --------------

    @_('')
    def parameters(self, p):
        return ''

    @_('INT NAME')
    def parameters(self, p):
        
        return p.NAME
    
    @_('INT NAME "," parameters')
    def parameters(self, p):
        return p.NAME + ' ' + p.parameters


    # ---------------- main ----------------

    @_('INT MAIN "(" ")" "{" statements "}"')
    def main(self, p):
        print('LOAD_CONST None')
        print('RETURN_VALUE')
        
    # ---------------- statements ----------------

    @_('statement statements')
    def statements(self, p):
        pass

    @_('')
    def statements(self, p):
        pass

    @_('function')
    def statements(self, p):
        pass
    
    @_('return_st')
    def statements(self, p):
        pass


    # ---------------- statement ----------------

    @_('while_st')
    def statement(self, p):
        print()
    
    @_('while_break_continue')
    def statement(self, p):
        print()

    @_('if_st')
    def statement(self, p):
        print()

    @_('printf')
    def statement(self, p):
        print()

    @_('declaration')
    def statement(self, p):
        print()

    @_('attribution')
    def statement(self, p):
        print()
    
    @_('call ";"')
    def statement(self, p):
        print()
    
    # ---------------- call ----------------

    @_('NAME')
    def init_call(self, p):
        print('# name(arguments);')
        print('LOAD_NAME', p.NAME)

    @_('init_call "(" arguments ")"')
    def call(self, p):
        print('#', p.arguments)
        print('CALL_FUNCTION', p.arguments)
        print()

    # ---------------- arguments ----------------

    @_('')
    def arguments(self, p):
        return 0

    @_('expression')
    def arguments(self, p):
        return 1

    @_('expression "," arguments')
    def arguments(self, p):
        return 1 + p.arguments

    # ---------------- while_st ----------------

    @_('WHILE "(" while_comp ")" "{" statements "}" end_while')
    def while_st(self, p):
        pass

    # ---------------- while_break ----------------
    @_('BREAKCONTINUE ";"')
    def while_break_continue(self, p):
        if (self.while_labels == []):
            self.show_error(f'"{p.BREAKCONTINUE}" outside of loop', p.lineno)
        elif (p.BREAKCONTINUE == 'break'):
            print(f'JUMP_ABSOLUTE NOT_WHILE_{self.while_labels[-1]}')
        else:
            print(f'JUMP_ABSOLUTE WHILE_{self.while_labels[-1]}')

    # ---------------- while_comp ----------------

    @_(' while_start expression COMP expression')
    def while_comp(self, p):
        print('COMPARE_OP', p.COMP)
        print(f'POP_JUMP_IF_FALSE NOT_WHILE_{self.while_count}')
        self.while_labels.append(self.while_count)
        self.while_count += 1

    # ---------------- while_start ----------------

    @_('')
    def while_start(self, p):
        print(f'WHILE_{self.while_count}:')  # imprime o identificador no início do bloco while
    
    # ---------------- end_while ----------------

    @_('')
    def end_while(self, p):
        label = self.while_labels.pop(-1)
        print(f'JUMP_ABSOLUTE WHILE_{label}')
        print(f'NOT_WHILE_{label}:')  #FR imprime o identificador no final do bloco while

    # ---------------- if_st ----------------

    @_('IF "(" if_comp ")" "{" statements "}" end_if')
    def if_st(self, p):
        pass

    # ---------------- if_comp ----------------

    @_('expression COMP expression')
    def if_comp(self, p):
        print('COMPARE_OP', p.COMP)
        print(f'POP_JUMP_IF_FALSE NOT_IF_{self.if_count}')
        self.if_labels.append(self.if_count)
        self.if_count += 1

    # ---------------- end_if ----------------

    @_('')
    def end_if(self, p):
        label = self.if_labels.pop(-1)
        print(f'NOT_IF_{label}:')  # imprime o identificador no final do bloco if

    # ---------------- printf ----------------

    @_('STRING')
    def printf_format(self, p):
        print("# printf(", p.STRING, ")")
        print('LOAD_GLOBAL', 'print')
        print('LOAD_CONST', p.STRING)

    @_('PRINTF "(" printf_format "," expression ")" ";"')
    def printf(self, p):
        print('BINARY_MODULO')
        print('CALL_FUNCTION', 1)
        print('POP_TOP')


    # ---------------- load_array ----------------

    @_('NAME')
    def load_array(self, p):
        if (p.NAME not in self.symbols_table):
            self.show_error(f"unknown variable '{p.NAME}'", p.lineno)
        print('LOAD_NAME', p.NAME)

    # ---------------- declaration ----------------
    
    @_('INT NAME "=" expression ";"')
    def declaration(self, p):
        if (p.NAME in self.symbols_table):
            self.show_error(f"cannot redeclare variable '{p.NAME}'", p.lineno)
        self.symbols_table.append(p.NAME)
        self.used_vars.append(False)
        print('STORE_NAME', p.NAME)
    
    # declaration of an array
    @_('INT NAME "[" "]" "=" "{" expressions "}" ";"')
    def declaration(self, p):
        if (p.NAME in self.symbols_table):
            self.show_error(f"cannot redeclare variable '{p.NAME}'", p.lineno)
        self.symbols_table.append(p.NAME)
        self.used_vars.append(False)
        print("#", p.NAME, p.expressions)
        print('BUILD_LIST', self.num_elements)
        self.num_elements = 0
        print('STORE_NAME', p.NAME)

    # ---------------- declaration empty array ----------------

    @_('INT NAME "[" array_size expression "]" ";"')
    def declaration(self, p):
        if (p.NAME in self.symbols_table):
            self.show_error(f"cannot redeclare variable '{p.NAME}'", p.lineno)
        self.symbols_table.append(p.NAME)
        self.used_vars.append(False)
        print('CALL_FUNCTION', 1)
        print('STORE_NAME', p.NAME)
    
    @_('')
    def array_size(self, p):
        print("LOAD_NAME array_zero")

    # ---------------- expressions ----------------


    @_('expressions "," expression')
    def expressions(self, p):
        self.num_elements += 1
        pass

    @_('expression')
    def expressions(self, p):
        self.num_elements += 1
        pass

    # ---------------- attribution ----------------

    @_('NAME "=" expression ";"')
    def attribution(self, p): 
        if (p.NAME not in self.symbols_table):
            self.show_error(f"unknown variable '{p.NAME}'", p.lineno)
        print('STORE_NAME', p.NAME)

    @_('load_array "[" expression "]" "=" expression ";"')
    def attribution(self, p):
        print('ROT_THREE')
        print("STORE_SUBSCR")

    # ---------------- expression ----------------

    @_('expression "+" term')
    def expression(self, p):
        print('BINARY_ADD')

    @_('expression "-" term')
    def expression(self, p):
        print('BINARY_SUBTRACT')

    @_('term')
    def expression(self, p):
        pass

    # ---------------- term ----------------

    @_('term "*" factor')
    def term(self, p):
        print('BINARY_MULTIPLY')

    @_('term "/" factor')
    def term(self, p):
        print('BINARY_FLOOR_DIVIDE')

    @_('term "%" factor')  # nova regra para o operador de módulo
    def term(self, p):
        print('BINARY_MODULO')

    @_('factor')
    def term(self, p):
        pass

    # ---------------- factor ----------------

    @_('NUMBER')
    def factor(self, p):
        print('LOAD_CONST', p.NUMBER)

    @_('"(" expression ")"')
    def factor(self, p):
        pass

    @_('NAME')
    def factor(self, p):
        if (p.NAME not in self.symbols_table):
            self.show_error(f"unknown variable '{p.NAME}'", p.lineno)
        self.used_vars[self.symbols_table.index(p.NAME)] = True
        print('LOAD_NAME', p.NAME)

    @_('NAME')
    def array_factor(self, p):
        if (p.NAME not in self.symbols_table):
            self.show_error(f"unknown variable '{p.NAME}'", p.lineno)
        self.used_vars[self.symbols_table.index(p.NAME)] = True
        print('LOAD_NAME', p.NAME)

    @_('array_factor "[" expression "]"')
    def factor(self, p):
        print("BINARY_SUBSCR")

    @_('call')
    def factor(self, p):
        pass

#################### MAIN ####################

lexer = ÇLexer()
parser = ÇParser()

if len(sys.argv) > 1:
    sys.stdin = open(sys.argv[1], 'r')
    
    if len(sys.argv) > 2:
        sys.stdout = open(sys.argv[2], 'w')

text = sys.stdin.read()
parser.parse(lexer.tokenize(text))
