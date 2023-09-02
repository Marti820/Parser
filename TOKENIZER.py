from typing import NamedTuple
import re 


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int
    
def tokenize(code):
    keywords = {'defVar','defProc','jump',
                'walk','front','right',
                'left','back','north',
                'south','west','east',
                'leap','turn','turnto',
                'drop','get','grab',
                'letGo','nop','if', 
                'else', 'while','repeat',
                'repeat','times','facing',
                'can','not'} #keywords 
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN',   r'='),           # Assignment operator
        ('END',      r';'),            # Statement terminator
        ('ID',       r'[A-Za-z][a-zA-Z0-9_]*'),    # Identifiers
        ('OP',       r'[+\-*/]'),      # Arithmetic operators
        ('NEWLINE',  r'\n'),           # Line endings
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ('LPAREN', r'\('),             # parentesis izq
        ('RPAREN', r'\)'),             # parentesis der
        ('COMA', r','),                # coma
        ('LBRACE', r'\{'),             # parentesis izq
        ('RBRACE', r'\}'),            # parentesis izq
        ('MISMATCH', r'.'),]            # Any other character
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    Lista_Tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        Lista_Tokens.append(Token(kind, value, line_num, column))
        #yield Token(kind, value, line_num, column)
    return Lista_Tokens   
#---------Pruebas-----------------------------------------------

code_2 = """defVar nom 0
defVar x 0
defVar y 0
defVar one 0
defVar n 0

defProc putCB (c , b )
{
drop( c ) ; 
letGo ( b ) ;
walk( n )
}

defProc goNorth ()
{
while can(walk(1 , north )) { walk(1 , north ) }
}
defProc goWest ()
{
if can(walk(1 , west ) ) { walk(1 , west ) } else {nop()}
}
{
jump (3 ,3) ;
putCB (2 ,1)
}
"""
code_3 = '''
dEfvaR n 0
'''
'''
a = tokenize(code_2)
for token in a:
    print(token)
'''
'''
class Parser(NamedTuple):
       
    type: str
    
def isJump(tokens):
    
    for i in tokens:
        if 
        
'''
code_4 = """
defVar nom 0
defVar x 0
defVar y 0
defVar one 0
defVar n 0
defVar 0 nosms
"""

#-----------------PARSER----------------

def Parse_general(codigo):
    Tokens = tokenize(codigo)
    currentToken = 0
    Variables = {}
    state = True
    
    while state == True and currentToken < len(Tokens):
        if Token_type(Tokens[currentToken]) == 'defVar':
           state, var, val = parse_DefVar(Tokens, currentToken, Variables)
           if state == True:
                Variables[var] = val
           else:
               break
        currentToken += 1 
    
    if state == True and currentToken == len(Tokens):
        print("CODIGO CORRECTO")
    else:
        print("CODIGO INCORRECTO")
    
def Token_type(token):
    return token[0]

def Token_val(token):
    return token[1]

def parse_DefVar(Tokens, currentToken, Variables):
    if Token_type(Tokens[currentToken + 1]) == 'ID' and Token_type(Tokens[currentToken + 2]) == 'NUMBER' and Token_val(Tokens[currentToken + 1]) not in Variables:
        return True, Token_val(Tokens[currentToken + 1]), Token_val(Tokens[currentToken + 2])
    else:
        return False, 0, 0
    
Parse_general(code_4)