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
"""

code_5 = """
defVar x 0
defVar y 1
defVar w 4
{
    jump(x,w);
    walk(x,north);
    walk(3);
    nop();

}
"""

#-----------------PARSER----------------
command_list = ['jump',
                'walk','leap','turn',
                'turnto','drop','get',
                'grab','letGo','nop',]

Direcciones = ['front','right',
                'left','back','north',
                'south','west','east',]

direcciones2 = ['front','right',
                'left','back',]

direcciones3 = ['north','south',
                'west','east',]

def Parse_general(codigo):
    #codigomin = codigo.lower()
    Tokens = tokenize(codigo)
    currentToken = 0
    Variables = {}
    state = True
    NewComands = {}
    
    if PreScan(Tokens) == False:
        state = False
    
    while state == True and currentToken < len(Tokens)-1:
        if Token_type(Tokens[currentToken]) == 'defVar':
           state, var, val = parse_DefVar(Tokens, currentToken, Variables)
           if state == True:
                Variables[var] = val
                
        if Token_type(Tokens[currentToken]) == 'defProc': #or (Token_type(Tokens[currentToken]) == 'LBRACE' and Token_type(Tokens[currentToken-1]) != 'RPAREN' ):
            state = ParseComplexComad(Tokens, currentToken, Variables)
        
        currentToken += 1 
    
    if state == True:
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

def Parse_simpleComand(Tokens, currentToken, Variables):
    if Token_type(Tokens[currentToken]) == 'jump' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and (Token_type(Tokens[currentToken + 4]) == 'NUMBER' or Token_type(Tokens[currentToken + 4]) == 'ID') and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'END' or Token_type(Tokens[currentToken + 6]) == 'RBRACE' ):
        if (Token_type(Tokens[currentToken + 2]) == 'ID' and Token_type(Tokens[currentToken + 4]) == 'ID'):
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() and Token_val(Tokens[currentToken + 4]) in Variables.keys():
                return True
        if (Token_type(Tokens[currentToken + 2]) == 'ID' and Token_type(Tokens[currentToken + 4]) == 'NUMBER'):
            if Token_val(Tokens[currentToken + 3]) in Variables.keys():
                return True
        if (Token_type(Tokens[currentToken + 2]) == 'NUMBER' and Token_type(Tokens[currentToken + 4]) == 'ID'):
            if  Token_val(Tokens[currentToken + 4]) in Variables.keys():
                return True
        if (Token_type(Tokens[currentToken + 2]) == 'NUMBER' and Token_type(Tokens[currentToken + 4]) == 'NUMBER'):
            return True
    if Token_type(Tokens[currentToken]) == 'walk' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'END' or Token_type(Tokens[currentToken + 6]) == 'RBRACE' ):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys():
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    if Token_type(Tokens[currentToken]) == 'walk' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'RPAREN' and (Token_type(Tokens[currentToken + 4]) == 'END' or Token_type(Tokens[currentToken + 4]) == 'RBRACE' ):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys():
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    if Token_type(Tokens[currentToken]) == 'leap' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'END' or Token_type(Tokens[currentToken + 6]) == 'RBRACE' ):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys():
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
        
    if Token_type(Tokens[currentToken]) == 'leap' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'RPAREN' and (Token_type(Tokens[currentToken + 4]) == 'END' or Token_type(Tokens[currentToken + 4]) == 'RBRACE' ):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys():
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    
    if Token_type(Tokens[currentToken]) == 'turn' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and Token_type(Tokens[currentToken + 2]) in direcciones2  and Token_type(Tokens[currentToken + 3]) == 'RPAREN' and (Token_type(Tokens[currentToken + 4]) == 'END' or Token_type(Tokens[currentToken + 4]) == 'RBRACE' ):
        return True
    
    if Token_type(Tokens[currentToken]) == 'drop' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'END' or Token_type(Tokens[currentToken + 6]) == 'RBRACE' ):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys():
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    
    if Token_type(Tokens[currentToken]) == 'get' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'END' or Token_type(Tokens[currentToken + 6]) == 'RBRACE' ):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys():
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True

    if Token_type(Tokens[currentToken]) == 'grab' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'END' or Token_type(Tokens[currentToken + 6]) == 'RBRACE' ):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys():
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    
    if Token_type(Tokens[currentToken]) == 'letGo' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'END' or Token_type(Tokens[currentToken + 6]) == 'RBRACE' ):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys():
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    
    if Token_type(Tokens[currentToken]) == 'nop' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and Token_type(Tokens[currentToken + 2]) == 'RPAREN' and (Token_type(Tokens[currentToken + 3]) == 'END' or Token_type(Tokens[currentToken + 3]) == 'RBRACE' ):
        return True
        
    else:
            False

def Parse_ASSIGN(Tokens, currentToken, Variables):
    
    if Token_type(Tokens[currentToken-1]) == 'ID' and Token_val(Tokens[currentToken-1]) in Variables.keys() and ((Token_type(Tokens[currentToken+1]) == 'ID' and Token_val(Tokens[currentToken-1]) in Variables.keys()) or Token_type(Tokens[currentToken+1]) == 'NUMBER') and (Token_type(Tokens[currentToken + 2]) == 'END' or Token_type(Tokens[currentToken + 2]) == 'RBRACE' ):
        return True  
    else:
        return False
   
def ParseComplexComad(Tokens, currentToken, Variables):
    
    if Token_type(Tokens[currentToken]) == 'defProc':
        parametros = []
        nombreProc = ""
        currentToken += 1
        state = True
        if Token_type(Tokens[currentToken]) == 'ID' and Token_val(Tokens[currentToken]) not in Variables:
            nombreProc = Token_val(Tokens[currentToken ])
            currentToken += 1 
        else: 
            return False
        
        if Token_type(Tokens[currentToken]) == 'LPAREN':
            currentToken += 1
            while Token_type(Tokens[currentToken]) != 'RPAREN':
                if Token_type(Tokens[currentToken]) == 'ID' and (Token_type(Tokens[currentToken+1])== 'COMA' or Token_type(Tokens[currentToken+1])== 'RPAREN'):
                    parametros.append(Token_val(Tokens[currentToken]))
                elif currentToken == len(Tokens)-1:
                    return False
                elif Token_type(Tokens[currentToken]) != 'ID' and Token_type(Tokens[currentToken]) != 'COMA':
                    return False
                currentToken +=1 
                
        if Token_type(Tokens[currentToken+1]) == 'LBRACE':
            currentToken += 1
        else:
            return False
        
        FinDelBloque = HallarFinDelBloqueDefProc(Tokens, currentToken)    
        for token in range(currentToken, FinDelBloque+1):
            if Token_type(Tokens[token]) in command_list:
                state = Parse_simpleComand(Tokens, currentToken, Variables)
 
            if Token_type(Tokens[token]) == 'ASSIGN':
                state = Parse_ASSIGN(Tokens, currentToken, Variables)
            #print(token)
            currentToken += 1
        return state
        
def HallarFinDelBloqueDefProc(Tokens, currentToken ):
    centinela = 0 
    currentToken_inicio = currentToken
    flag = True        
            
    while flag == True:
        if  Token_type(Tokens[currentToken_inicio]) == 'LBRACE':
            centinela += 1 
        if Token_type(Tokens[currentToken_inicio]) == 'RBRACE':
            centinela -= 1
        if centinela == 0:
            flag = False
            return currentToken_inicio
        if centinela < 0:
            return False
        if currentToken_inicio == len(Tokens)-1 and centinela != 0:
            return False
        #print('corriendo')
        currentToken_inicio +=1
        
def PreScan(Tokens):
    centinela = 0
    currentToken_inicio = 0
    flag = True
    while flag == True:
        if  Token_type(Tokens[currentToken_inicio]) == 'LBRACE':
            centinela += 1 
        if Token_type(Tokens[currentToken_inicio]) == 'RBRACE':
            centinela -= 1
        if centinela < 0:
            return False
        if currentToken_inicio == len(Tokens)-1 and centinela != 0:
            return False
        if currentToken_inicio == len(Tokens)-1 and centinela == 0:
            return True
        #print('corriendo')
        currentToken_inicio +=1
        
code_6='''
defProc putCB (c , b){
    {
        walk(3)
    }
}
'''
'''
defVar x 0
{
    x =3
}

'''

#print(PreScan(tokenize(code_6)))
    
    
'''
command_list = ['jump',
                'walk','leap','turn',
                'turnto','drop','get',
                'grab','letGo','nop','ASSIGN']   
'''
Parse_general(code_6)
'''
a = tokenize(code_5)
for token in a:
    print(token)
'''