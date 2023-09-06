from typing import NamedTuple
import re 


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int
    
def tokenize(code):
    keywords = {'defvar','defproc','jump',
                'walk','front','right',
                'left','back','north',
                'south','west','east',
                'leap','turn','turnto',
                'drop','get','grab',
                'letgo','nop','if', 
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
        ('COLON', r':'),                # dos puntos 
        ('MISMATCH', r'.')]             # Any other character
       
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

#-----------------PARSER----------------
command_list = ['jump',
                'walk','leap','turn',
                'turnto','drop','get',
                'grab','letgo','nop',]

Direcciones = ['front','right',
                'left','back','north',
                'south','west','east',]

direcciones2 = ['front','right',
                'left','back',]

direcciones3 = ['north','south',
                'west','east',]

def Parse_general(codigo):
    codigo = codigo.lower()
    Tokens = tokenize(codigo)
    currentToken = 0
    Variables = {}
    state = True
    NewComands = {}
    
    if PreScan(Tokens) == False:
        state = False
    if PreScan2(Tokens) == False:
        state = False
    if PreScan3(Tokens) == False:
        state = False
    
    while state == True and currentToken < len(Tokens)-1:
        if Token_type(Tokens[currentToken]) == 'defvar':
           state, var, val = parse_DefVar(Tokens, currentToken, Variables)
           if state == True:
                Variables[var] = val
                
        if Token_type(Tokens[currentToken]) == 'defproc' or (Token_type(Tokens[currentToken]) == 'LBRACE'):
            if Token_type(Tokens[currentToken]) == 'defproc':
                no = []
                state, definiciones = ParseComplexComad(Tokens, currentToken, Variables, NewComands, no)
                NewComands.update(definiciones)
            elif Token_type(Tokens[currentToken]) == 'LBRACE':
                param = verificarParametros(Tokens, currentToken)
                if param[0] == True:
                    state = ParseComplexComad(Tokens, currentToken, Variables, NewComands, param[1])
                elif param[0] == False:
                    no = []
                    state = ParseComplexComad(Tokens, currentToken, Variables, NewComands, no)
                    
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

def Parse_simpleComand(Tokens, currentToken, Variables, parametros):
    if Token_type(Tokens[currentToken]) == 'jump' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and (Token_type(Tokens[currentToken + 4]) == 'NUMBER' or Token_type(Tokens[currentToken + 4]) == 'ID') and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'END' or Token_type(Tokens[currentToken + 6]) == 'RBRACE' or Token_type(Tokens[currentToken + 6]) == 'RPAREN' ):
        if (Token_type(Tokens[currentToken + 2]) == 'ID' and Token_type(Tokens[currentToken + 4]) == 'ID'):
            if Token_val((Tokens[currentToken + 2]) in Variables.keys() or Token_val((Tokens[currentToken + 2])) in parametros) and (Token_val(Tokens[currentToken + 4]) in Variables.keys() or Token_val((Tokens[currentToken + 4])) in parametros):
                return True
        if (Token_type(Tokens[currentToken + 2]) == 'ID' and Token_type(Tokens[currentToken + 4]) == 'NUMBER'):
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if (Token_type(Tokens[currentToken + 2]) == 'NUMBER' and Token_type(Tokens[currentToken + 4]) == 'ID'):
            if  Token_val(Tokens[currentToken + 4]) in Variables.keys() or Token_val(Tokens[currentToken + 4]) in parametros:
                return True
        if (Token_type(Tokens[currentToken + 2]) == 'NUMBER' and Token_type(Tokens[currentToken + 4]) == 'NUMBER'):
            return True
    elif Token_type(Tokens[currentToken]) == 'walk' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'END' or Token_type(Tokens[currentToken + 6]) == 'RBRACE' or Token_type(Tokens[currentToken + 6]) == 'RPAREN'):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
            else:
                return False
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    elif Token_type(Tokens[currentToken]) == 'walk' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'RPAREN' and (Token_type(Tokens[currentToken + 4]) == 'END' or Token_type(Tokens[currentToken + 4]) == 'RBRACE' or Token_type(Tokens[currentToken + 4]) == 'RPAREN'):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
            else:
                False
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    elif Token_type(Tokens[currentToken]) == 'leap' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'END' or Token_type(Tokens[currentToken + 6]) == 'RBRACE'or Token_type(Tokens[currentToken + 6]) == 'RPAREN' ):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
        
    elif Token_type(Tokens[currentToken]) == 'leap' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'RPAREN' and (Token_type(Tokens[currentToken + 4]) == 'END' or Token_type(Tokens[currentToken + 4]) == 'RBRACE' or Token_type(Tokens[currentToken + 4]) == 'RPAREN' ):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    
    elif Token_type(Tokens[currentToken]) == 'turn' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and Token_type(Tokens[currentToken + 2]) in direcciones2  and Token_type(Tokens[currentToken + 3]) == 'RPAREN' and (Token_type(Tokens[currentToken + 4]) == 'END' or Token_type(Tokens[currentToken + 4]) == 'RBRACE' or Token_type(Tokens[currentToken + 4]) == 'RPAREN'):
        return True
    
    elif Token_type(Tokens[currentToken]) == 'drop' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'RPAREN' and (Token_type(Tokens[currentToken + 4]) == 'END' or Token_type(Tokens[currentToken + 4]) == 'RBRACE' or Token_type(Tokens[currentToken + 4]) == 'RPAREN'):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    
    elif Token_type(Tokens[currentToken]) == 'get' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'END' or Token_type(Tokens[currentToken + 6]) == 'RBRACE' or Token_type(Tokens[currentToken + 6]) == 'RPAREN'):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True

    elif Token_type(Tokens[currentToken]) == 'grab' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'END' or Token_type(Tokens[currentToken + 6]) == 'RBRACE' or Token_type(Tokens[currentToken + 6]) == 'RPAREN'):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    
    elif Token_type(Tokens[currentToken]) == 'letgo' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'RPAREN' and (Token_type(Tokens[currentToken + 4]) == 'END' or Token_type(Tokens[currentToken + 4]) == 'RBRACE' or Token_type(Tokens[currentToken + 4]) == 'RPAREN'):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    
    elif Token_type(Tokens[currentToken]) == 'nop' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and Token_type(Tokens[currentToken + 2]) == 'RPAREN' and (Token_type(Tokens[currentToken + 3]) == 'END' or Token_type(Tokens[currentToken + 3]) == 'RBRACE' or Token_type(Tokens[currentToken + 6]) == 'RPAREN'):
        return True
        
    else:
        return False

def Parse_ASSIGN(Tokens, currentToken, Variables, parametros):
    
    if Token_type(Tokens[currentToken-1]) == 'ID' and Token_val(Tokens[currentToken-1]) in Variables.keys() and ((Token_type(Tokens[currentToken+1]) == 'ID' and Token_val(Tokens[currentToken+1]) in Variables.keys()) or Token_type(Tokens[currentToken+1]) == 'NUMBER' or Token_val(Tokens[currentToken+1]) in parametros) and (Token_type(Tokens[currentToken + 2]) == 'END' or Token_type(Tokens[currentToken + 2]) == 'RBRACE' ):
        return True  
    else:
        return False
   
def ParseComplexComad(Tokens, currentToken, Variables, newConmands, parametros_2):
    
    if Token_type(Tokens[currentToken]) == 'defproc':
        parametros = []
        nombreProc = ""
        currentToken += 1
        state = True
        definicion = {}
        if Token_type(Tokens[currentToken]) == 'ID' and Token_val(Tokens[currentToken]) not in Variables:
            nombreProc = Token_val(Tokens[currentToken ])
            definicion[nombreProc] = 0
            currentToken += 1 
        else: 
            return False,0
        
        if Token_type(Tokens[currentToken]) == 'LPAREN':
            currentToken += 1
            while Token_type(Tokens[currentToken]) != 'RPAREN':
                if Token_type(Tokens[currentToken]) == 'ID' and (Token_type(Tokens[currentToken+1])== 'COMA' or Token_type(Tokens[currentToken+1])== 'RPAREN'):
                    parametros.append(Token_val(Tokens[currentToken]))
                    #Variables[Token_val(Tokens[currentToken])] = 0 
                elif currentToken == len(Tokens)-1:
                    return False, 0
                elif Token_type(Tokens[currentToken]) != 'ID' and Token_type(Tokens[currentToken]) != 'COMA':
                    return False, 0
                currentToken +=1 
        else: 
            return False, 0
        definicion[nombreProc] = len(parametros)
                
        if Token_type(Tokens[currentToken+1]) == 'LBRACE':
            currentToken += 1
        else:
            return False
        
        newConmands2 = newConmands
        newConmands2.update(definicion)
        
        FinDelBloque = HallarFinDelBloqueDefProc(Tokens, currentToken)    
        for token in range(currentToken, FinDelBloque+1):
            if Token_type(Tokens[token]) in command_list:
                state = Parse_simpleComand(Tokens, currentToken, Variables, parametros)
                if state == False:
                    break
            if Token_type(Tokens[token]) == 'ASSIGN':
                state = Parse_ASSIGN(Tokens, currentToken, Variables)
                if state == False:
                    break
            if Token_type(Tokens[token]) == 'ID' and Token_val(Tokens[token]) in newConmands2.keys():
                state = ParseNewCommand(Tokens, currentToken, Variables,parametros, newConmands, Token_val(Tokens[token]))
                if state == False:
                    break
            if Token_type(Tokens[token]) == 'ID' and Token_val(Tokens[token]) not in newConmands.keys() and Token_val(Tokens[token]) not in Variables.keys() and Token_val(Tokens[token]) not in parametros:
                state = False
                break
            if Token_type(Tokens[token]) == 'while':
                state = ParseCond1(Tokens, currentToken, Variables, parametros)
                if state == False:
                    break
            if Token_type(Tokens[token]) == 'if':
                state = parseIF(Tokens, currentToken, Variables, parametros)
                if state == False:
                    break
                
            if  Token_type(Tokens[token]) == 'repeat':
                state = parseRepeatTimes(Tokens, currentToken, Variables)
                if state == False:
                    break

            #print(token)

            currentToken += 1
        return state, definicion

    if Token_type(Tokens[currentToken]) == 'LBRACE':
        parametros = parametros_2
        FinDelBloque = HallarFinDelBloqueDefProc(Tokens, currentToken)    
        for token in range(currentToken, FinDelBloque+1):
            
            if Token_type(Tokens[token]) in command_list:
                state = Parse_simpleComand(Tokens, currentToken, Variables, parametros)
                if state == False:
                    break
            if Token_type(Tokens[token]) == 'ASSIGN':
                state = Parse_ASSIGN(Tokens, currentToken, Variables, parametros)
                if state == False:
                    break
            if Token_type(Tokens[token]) == 'ID' and Token_val(Tokens[token]) in newConmands.keys():
                state = ParseNewCommand(Tokens, currentToken, Variables, parametros, newConmands, Token_val(Tokens[token]))
                if state == False:
                    break
            if Token_type(Tokens[token]) == 'ID' and Token_val(Tokens[token]) not in newConmands.keys() and Token_val(Tokens[token]) not in Variables.keys() and Token_val(Tokens[token]) not in parametros:
                state = False
                break
            if Token_type(Tokens[token]) == 'while':
                state = ParseCond1(Tokens, currentToken, Variables,parametros )
                if state == False:
                    break
            if Token_type(Tokens[token]) == 'if':
                state = parseIF(Tokens, currentToken, Variables, parametros)
                if state == False:
                    break
            if  Token_type(Tokens[token]) == 'repeat':
                state = parseRepeatTimes(Tokens, currentToken, Variables)
                if state == False:
                    break
            #print(token)
            
            currentToken += 1
            
        return state
        
def ParseNewCommand(Tokens, currentToken, Variables, parametros ,NewComands, nombreComm):
    
    NumPar = (NewComands[nombreComm] * 2)+1
    currentToken += 1
    if NumPar != 1: 
        for token in range(currentToken, currentToken + NumPar - 1):
            if (Token_type(Tokens[token]) == 'ID' and (Token_val(Tokens[token]) in Variables.keys() or Token_val(Tokens[token]) in parametros) or Token_type(Tokens[token]) == 'NUMBER') and (token-currentToken)%2 != 0:
                state = True
            elif Token_type(Tokens[token]) == 'COMA' and (token-currentToken)%2 == 0:
                state = True
            elif token == currentToken and Token_type(Tokens[token]) == 'LPAREN':
                state = True
            elif token == currentToken + NumPar - 1  and Token_type(Tokens[token]) == 'RPAREN' and ((Token_type(Tokens[token + 1]) == 'END' or Token_type(Tokens[token + 1]) == 'RBRACE' )):
                state = True
            else:
                state = False
                break 
    else:
        if Token_type(Tokens[currentToken]) == 'LPAREN' and Token_type(Tokens[currentToken+1]) == 'RPAREN' and ((Token_type(Tokens[currentToken + 2]) == 'END' or Token_type(Tokens[currentToken + 2]) == 'RBRACE' )):
            state = True
        else:
            state = False
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
        
def PreScan2(Tokens):
    centinela = 0
    currentToken_inicio = 0
    flag = True
    while flag == True:
        if  Token_type(Tokens[currentToken_inicio]) == 'LPAREN':
            centinela += 1 
        if Token_type(Tokens[currentToken_inicio]) == 'RPAREN':
            centinela -= 1
        if centinela < 0:
            return False
        if currentToken_inicio == len(Tokens)-1 and centinela != 0:
            return False
        if currentToken_inicio == len(Tokens)-1 and centinela == 0:
            return True
        if Token_type(Tokens[currentToken_inicio]) == 'LPAREN' and Token_type(Tokens[currentToken_inicio+1]) == 'LPAREN':
            return False
        #print('corriendo')
        currentToken_inicio +=1        
        
def PreScan3(Tokens):
    flag = True 
    currentToken_inicio = 0
    while flag == True:
        if currentToken_inicio != len(Tokens)-1:
            if  Token_type(Tokens[currentToken_inicio]) == 'END' and Token_type(Tokens[currentToken_inicio+1]) == 'END':
                return False
        if currentToken_inicio == len(Tokens)-1:
            return True
        currentToken_inicio += 1
        
def Parse_CondSimpleComand(Tokens, currentToken, Variables, parametros):
    if Token_type(Tokens[currentToken]) == 'jump' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and (Token_type(Tokens[currentToken + 4]) == 'NUMBER' or Token_type(Tokens[currentToken + 4]) == 'ID') and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and  Token_type(Tokens[currentToken + 6]) == 'RPAREN' :
        if (Token_type(Tokens[currentToken + 2]) == 'ID' and Token_type(Tokens[currentToken + 4]) == 'ID'):
            if (Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros ) and (Token_val(Tokens[currentToken + 4]) in Variables.keys() or Token_val(Tokens[currentToken + 4]) in parametros):
                return True
        if (Token_type(Tokens[currentToken + 2]) == 'ID' and Token_type(Tokens[currentToken + 4]) == 'NUMBER'):
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if (Token_type(Tokens[currentToken + 2]) == 'NUMBER' and Token_type(Tokens[currentToken + 4]) == 'ID'):
            if  Token_val(Tokens[currentToken + 4]) in Variables.keys() or Token_val(Tokens[currentToken + 4]) in parametros:
                return True
        if (Token_type(Tokens[currentToken + 2]) == 'NUMBER' and Token_type(Tokens[currentToken + 4]) == 'NUMBER'):
            return True
    elif Token_type(Tokens[currentToken]) == 'walk' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'RPAREN'):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
            else:
                return False
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    elif Token_type(Tokens[currentToken]) == 'walk' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'RPAREN' and Token_type(Tokens[currentToken + 4]) == 'RPAREN':
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
            else:
                False
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    elif Token_type(Tokens[currentToken]) == 'leap' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'RPAREN' ):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
        
    elif Token_type(Tokens[currentToken]) == 'leap' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'RPAREN' and (Token_type(Tokens[currentToken + 4]) == 'RPAREN'):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros :
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    
    elif Token_type(Tokens[currentToken]) == 'turn' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and Token_type(Tokens[currentToken + 2]) in direcciones2  and Token_type(Tokens[currentToken + 3]) == 'RPAREN' and (Token_type(Tokens[currentToken + 4]) == 'RPAREN'):
        return True
    
    elif Token_type(Tokens[currentToken]) == 'drop' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'RPAREN' and (Token_type(Tokens[currentToken + 4]) == 'END' or Token_type(Tokens[currentToken + 4]) == 'RBRACE' or Token_type(Tokens[currentToken + 4]) == 'RPAREN'):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    
    elif Token_type(Tokens[currentToken]) == 'get' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'RPAREN'):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True

    elif Token_type(Tokens[currentToken]) == 'grab' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'RPAREN'):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    
    elif Token_type(Tokens[currentToken]) == 'letgo' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and (Token_type(Tokens[currentToken + 2]) == 'NUMBER' or Token_type(Tokens[currentToken + 2]) == 'ID') and Token_type(Tokens[currentToken + 3]) == 'COMA' and Token_type(Tokens[currentToken + 4]) in Direcciones and Token_type(Tokens[currentToken + 5]) == 'RPAREN' and (Token_type(Tokens[currentToken + 6]) == 'RPAREN' ):
        if Token_type(Tokens[currentToken + 2]) == 'ID':
            if Token_val(Tokens[currentToken + 2]) in Variables.keys() or Token_val(Tokens[currentToken + 2]) in parametros:
                return True
        if Token_type(Tokens[currentToken + 2]) == 'NUMBER':
            return True
    
    elif Token_type(Tokens[currentToken]) == 'nop' and Token_type(Tokens[currentToken + 1]) == 'LPAREN' and Token_type(Tokens[currentToken + 2]) == 'RPAREN' and (Token_type(Tokens[currentToken + 3]) == 'RPAREN'):
        return True
        
    else:
        return False        
 
def ParseCond1(Tokens, currentToken, Variables, parametros):
    if Token_type(Tokens[currentToken+1]) == 'facing':
        if Token_type(Tokens[currentToken+2]) == 'LPAREN':
             if Token_val(Tokens[currentToken+3]) in direcciones3:
                    state =  True
    elif Token_type(Tokens[currentToken+1]) == 'can':
        if Token_type(Tokens[currentToken+2]) == 'LPAREN':
            if Token_val(Tokens[currentToken+3]) in command_list:
                 if ParseCondNOT(Tokens,currentToken+3,Variables,parametros)==True:
                    state = True
                
    elif Token_type(Tokens[currentToken+1]) == 'not':
        if Token_type(Tokens[currentToken+2]) == 'COLON':
            if ParseCondNOT(Tokens,currentToken+3,Variables, parametros)==True:
                    state = True
        
    else:
        return False
     
    if state == True:
        flag = False
        while flag == False:
            if currentToken == len(Tokens)-1:
                break
            if currentToken != len(Tokens)-1:
                if Token_type(Tokens[currentToken]) == 'LBRACE':
                    final = HallarFinDelBloqueDefProc(Tokens, currentToken)
                    if Token_type(Tokens[final + 1]) == 'END' and Token_type(Tokens[final + 2]) == 'RBRACE':
                        flag = True        
                    else:
                        break

            currentToken += 1
        if flag == False:
            return False
    else:
        return False   
    
    
def ParseCondNOT(Tokens, currentToken, Variables, parametros):
    if Token_type(Tokens[currentToken]) == 'facing':
        if Token_type(Tokens[currentToken+1]) == 'LPAREN':
             if Token_val(Tokens[currentToken+2]) in direcciones3:
                     return True
    elif Token_type(Tokens[currentToken]) == 'can':
        if Token_type(Tokens[currentToken+1]) == 'LPAREN':
            if Token_val(Tokens[currentToken+2]) in command_list:
                 if Parse_CondSimpleComand(Tokens,currentToken+2,Variables, parametros)==True:
                    return True
    
    else:
       return True

def parseIF(Tokens, currentToken, Variables, parametros):
    if Token_type(Tokens[currentToken+1]) == 'facing':
        if Token_type(Tokens[currentToken+2]) == 'LPAREN':
             if Token_val(Tokens[currentToken+3]) in direcciones3:
                     state = True
    elif Token_type(Tokens[currentToken+1]) == 'can':
        if Token_type(Tokens[currentToken+2]) == 'LPAREN':
            if Token_val(Tokens[currentToken+3]) in command_list:
                 if ParseCondNOT(Tokens,currentToken+3,Variables, parametros)==True:
                    state = True
                
    elif Token_type(Tokens[currentToken+1]) == 'not':
        if Token_type(Tokens[currentToken+2]) == 'COLON':
            if ParseCondNOT(Tokens,currentToken+3,Variables, parametros)==True:
                    state = True
        
    else:
        return = False
    
    if state == True:
        flag = False
        while flag == False:
            if currentToken == len(Tokens)-1:
                break
            if currentToken != len(Tokens)-1:
                if Token_type(Tokens[currentToken]) == 'LBRACE':
                    final = HallarFinDelBloqueDefProc(Tokens, currentToken)
                    if Token_type(Tokens[final + 1]) == 'else' and Token_type(Tokens[final + 2]) == 'LBRACE':
                            final2  = HallarFinDelBloqueDefProc(Tokens, final +2)
                            if Token_type(Tokens[final2 + 1]) == 'END' or Token_type(Tokens[final2 + 1]) == 'RBRACE':
                                flag = True
                            else:
                                break
                    else:
                        break

            currentToken += 1
        if flag == False:
            return False
    else:
        return False
    
def parseRepeatTimes(Tokens, currentToken, Variables, parametros):
    
     if Token_type(Tokens[currentToken+1]) == 'NUMBER' or Token_val(Tokens[currentToken+1]) in Variables.keys() or Token_val(Tokens[currentToken+1]) in parametros:
        if Token_type(Tokens[currentToken+2]) == 'times':
             if Token_type(Tokens[currentToken+3]) == 'LBRACE':
                     return True

def verificarParametros(Tokens, currentToken):
    pos_in = currentToken
    flag = True
    continuar = True
    esta = False
    while flag:
        if Token_type(Tokens[currentToken]) == 'defproc':
            flag2 = True
            posdefproc = currentToken
            while flag2:
                if Token_type(Tokens[currentToken]) == 'LBRACE':
                    flag = False
                    continuar = True
                    break
                currentToken += 1
            if continuar ==  True:
                break
        if currentToken == 0:
            flag = False
            continuar = False
        currentToken -=1
            
    if continuar == True:
        finBloque = HallarFinDelBloqueDefProc(Tokens,currentToken)
        if pos_in > posdefproc and finBloque > pos_in:
            esta = True
        
    if esta == True:
        Parametros =  hallarParametros(Tokens, posdefproc+2)
        return esta, Parametros
    else:
        nada = []
        return esta, [] 
    
def hallarParametros(Tokens, currentToken):
    parametros = []
    if Token_type(Tokens[currentToken]) == 'LPAREN':
            currentToken += 1
            while Token_type(Tokens[currentToken]) != 'RPAREN':
                if Token_type(Tokens[currentToken]) == 'ID' and (Token_type(Tokens[currentToken+1])== 'COMA' or Token_type(Tokens[currentToken+1])== 'RPAREN'):
                    parametros.append(Token_val(Tokens[currentToken]))
                    #Variables[Token_val(Tokens[currentToken])] = 0 
                elif currentToken == len(Tokens)-1:
                    return False, 0
                elif Token_type(Tokens[currentToken]) != 'ID' and Token_type(Tokens[currentToken]) != 'COMA':
                    return False, 0
                currentToken +=1 
    return parametros

#----------------------------Main funcion-----------------------
def mainFunction(Archivo):
    with open(Archivo) as file:
        file_contents = file.read()
    file.close()
    print(Parse_general(file_contents))
    return None
mainFunction('prueba.txt')
