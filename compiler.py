def check_line_token(brutecode,termos):
    line=1
    last_term=0
    for i_index,i in enumerate(termos):
        sts = brutecode.find(i,last_term)
        fnd = brutecode.find('\n',last_term,sts)
        while fnd != -1:
            line += 1
            fnd = brutecode.find('\n',fnd+1,sts)
        last_term=sts
        termos[i_index]=[termos[i_index],line]

def lexiconanal(brutecode):
    import nltk
    import re

    global inputlist
    global preservada
    
    mktoken = nltk.WordPunctTokenizer()
    termos = mktoken.tokenize(brutecode)
    #print(" ============== \n Lista de Tokens \n =================")
    preservada = {'if', 'then', 'while', 'do', 'write', 'read', 'else', 'begin', 'end', 'var', 'real', 'integer', 'procedure'}
    ssimples = {'(', ')', '*', '/', '+', '-', '>', '<', '$', ';', ':', ',', '.', '='}
    tratar = {');'}
    sduplo = {'<>', '>=', '<=', ':='}
    com1 = False
    com2 = False
    numero = None
    numero_real = None
    check_line_token(brutecode,termos)


    for [i,line] in termos:    
        if com1 == True or com2 == True:
            if i == '*/':
                com1 = False
                #print(i + ', Comentário')
            elif i == '}':
                com2 = False
                #print(i + ', Comentário')
                #print(i + ', Comentário')
        else:
            if numero!=None and numero_real==None and i!='.':
                #print(i + ',  Numero Inteiro')
                numero = None
                inputlist.append([i,line])
            if numero == None and numero_real == None:
                if i == '/*':
                    com1 = True
                    #print(i + ', Comentário')
                elif i == '{':
                    com2 = True
                    #print(i + ', Comentário')
                elif i in preservada:
                    #print(i + ', Palavra Reservada')
                    inputlist.append([i,line])
                elif i in tratar:
                    #print(i[0] + ', Simbolo Simples')
                    inputlist.append([i[0],line])
                    #print(i[1] + ', Simbolo Simples')
                    inputlist.append([i[1],line])
                elif i in ssimples:
                    #print(i + ', Simbolo Simples')
                    inputlist.append([i,line])
                elif i in sduplo:
                    #print(i + ', Simbolo Duplo')
                    inputlist.append([i,line])    
                elif re.match('\w+', i) and re.match('[a-zA-Z]', i[0]):
                    #print(i + ',  Identificador')
                    inputlist.append([i,line])
                elif i.isdigit():
                    numero = i
                else:
                    #print(str(i) + ',  token inválido na linha: ' + str(line))
                    return(0)
            elif numero_real == None and i=='.':
                numero_real = str(numero)+i
            elif numero_real!=None and i.isdigit():
                numero_real = numero_real+str(i)
                #print(numero_real + ',  Numero Real')
                inputlist.append([numero_real,line])
                numero = None
                numero_real = None               
            else:
                #print(numero_real + ',  token inválido na linha: ' + str(line))
                return(0)
    print('\nLexicon Accepted! \n')
    return (1)

def syntaxanal():
    import re
    global error
    errorac = []

    def programa():
        global error

        if inputlist[0][0]=='program':
            inputlist.pop(0)
            if re.match('\w+', inputlist[0][0]) and re.match('[a-zA-Z]', inputlist[0][0][0]) and inputlist[0][0] not in preservada:
                inputlist.pop(0)
                if corpo():
                    if inputlist[0][0]=='.':
                        inputlist.pop(0)
                        return(1)
                    else:
                        error = "Invalid Syntax - expected '.' in line " + str(inputlist[0][1])
                        return(0)
                else:
                    return(0)
            else:
                error = "Invalid Syntax - expected ident in line " + str(inputlist[0][1])
                return(0)
        else:
            error = "Invalid Syntax - expected 'program' in line " + str(inputlist[0][1])
            return(0)
    
    def corpo():
        global error

        if dc():
            if inputlist[0][0]=='begin':
                inputlist.pop(0)
                if comandos():
                    if inputlist[0][0]=='end':
                        inputlist.pop(0)
                        return(1)
                    else:
                        error = "Invalid Syntax - expected 'end' in line " + str(inputlist[0][1])
                        return(0)
                else:
                    return(0)
            else:
                error = "Invalid Syntax - expected 'begin' in line " + str(inputlist[0][1])
                return(0)
        else:
            return(0)

    def dc():
        global error

        if dc_v():
            if mais_dc():
                return(1)
            else:
                return(0)
        elif dc_p():
            if mais_dc():
                return(1)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def mais_dc():
        global error

        if inputlist[0][0]==';':
            inputlist.pop(0)
            if dc():
                return(1)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def dc_v():
        global error

        if inputlist[0][0]=='var':
            inputlist.pop(0)
            if variaveis():
                if inputlist[0][0]==':':
                    inputlist.pop(0)
                    if tipo_var():
                        return(1)
                    else:
                        return(0)
                else:
                    error = "Invalid Syntax - expected ':' in line " + str(inputlist[0][1])
                    return(0)
            else:
                return(0)
        else:
            errorac.append("Invalid Syntax - expected 'var' in line " + str(inputlist[0][1]))
            return(0)

    def tipo_var():
        global error

        if inputlist[0][0]=='real' or inputlist[0][0]=='integer':
            inputlist.pop(0)
            return(1)
        else:
            errorac.append("Invalid Syntax - expected 'real' or 'integer' in line " + str(inputlist[0][1]))
            return(0)

    def variaveis():
        global error

        if re.match('\w+', inputlist[0][0]) and re.match('[a-zA-Z]', inputlist[0][0][0]) and inputlist[0][0] not in preservada:
            inputlist.pop(0)
            if mais_var():
                return(1)
            else:
                return(0)
        else:
            errorac.append("Invalid Syntax - expected ident in line " + str(inputlist[0][1]))
            return(0)

    def mais_var():
        global error

        if inputlist[0][0]==',':
            inputlist.pop(0)
            if variaveis():
                return(1)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def dc_p():
        global error

        if inputlist[0][0]=='procedure':
            inputlist.pop(0)
            if re.match('\w+', inputlist[0][0]) and re.match('[a-zA-Z]', inputlist[0][0][0]) and inputlist[0][0] not in preservada:
                inputlist.pop(0)
                if parametros():
                    if corpo_p():
                        return(1)
                    else:
                        return(0)
                else:
                    return(0)
            else:
                error = "Invalid Syntax - expected ident in line " + str(inputlist[0][1])
                return(0)
        else:
            errorac.append("Invalid Syntax - expected 'procedure' in line " + str(inputlist[0][1]))
            return(0)

    def parametros():
        global error

        if inputlist[0][0]=='(':
            inputlist.pop(0)
            if lista_par():
                if inputlist[0][0]==')':
                    inputlist.pop(0)
                    return(1)
                else:
                    error = "Invalid Syntax - expected ')' in line " + str(inputlist[0][1])
                    return(0)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def lista_par():
        global error

        if variaveis():
            if inputlist[0][0]==':':
                inputlist.pop(0)
                if tipo_var():
                    if mais_par():
                        return(1)
                    else:
                        return(0)
                else:
                    return(0)
            else:
                error = "Invalid Syntax - expected ':' in line " + str(inputlist[0][1])
                return(0)
        else:
            return(0)

    def mais_par():
        global error

        if inputlist[0][0]==';':
            inputlist.pop(0)
            if lista_par():
                return(1)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def corpo_p():
        global error

        if dc_loc():
            if inputlist[0][0]=='begin':
                inputlist.pop(0)
                if comandos():
                    if inputlist[0][0]=='end':
                        inputlist.pop(0)
                        return(1)
                    else:
                        error = "Invalid Syntax - expected 'end' in line " + str(inputlist[0][1])
                        return(0)
                else:
                    return(0)
            else:
                error = "Invalid Syntax - expected 'begin' in line " + str(inputlist[0][1])
                return(0)
        else:
            return(0)

    def dc_loc():
        global error

        if dc_v():
            if mais_dcloc():
                return(1)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def mais_dcloc():
        global error

        if inputlist[0][0]==';':
            inputlist.pop(0)
            if dc_loc():
                return(1)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def lista_arg():
        global error

        if inputlist[0][0]=='(':
            inputlist.pop(0)
            if argumentos():
                if inputlist[0][0]==')':
                    inputlist.pop(0)
                    return(1)
                else:
                    error = "Invalid Syntax - expected ')' in line " + str(inputlist[0][1])
                    return(0)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def argumentos():
        global error

        if re.match('\w+', inputlist[0][0]) and re.match('[a-zA-Z]', inputlist[0][0][0]) and inputlist[0][0] not in preservada:
            inputlist.pop(0)
            if mais_ident():
                return(1)
            else:
                return(0)
        else:
            errorac.append("Invalid Syntax - expected ident in line " + str(inputlist[0][1]))
            return(0)

    def mais_ident():
        global error

        if inputlist[0][0]==';':
            inputlist.pop(0)
            if argumentos():
                return(1)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def pfalsa():
        global error

        if inputlist[0][0]=='else':
            inputlist.pop(0)
            if comandos():
                return(1)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def comandos():
        if comando():
            if mais_comandos():
                return(1)
            else:
                return(0)
        else:
            return(0)

    def mais_comandos():
        global error

        if inputlist[0][0]==';':
            inputlist.pop(0)
            if comandos():
                return(1)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def comando():
        global error

        if inputlist[0][0]=='read':
            inputlist.pop(0)
            if inputlist[0][0]=='(':
                inputlist.pop(0)
                if variaveis():
                    if inputlist[0][0]==')':
                        inputlist.pop(0)
                        return(1)
                    else:
                        error = "Invalid Syntax - expected ')' in line " + str(inputlist[0][1])
                        return(0)
                else:
                    return(0)
            else:
                error = "Invalid Syntax - expected '(' in line " + str(inputlist[0][1])
                return(0)
        elif inputlist[0][0]=='write':
            inputlist.pop(0)
            if inputlist[0][0]=='(':
                inputlist.pop(0)
                if variaveis():
                    if inputlist[0][0]==')':
                        inputlist.pop(0)
                        return(1)
                    else:
                        error = "Invalid Syntax - expected ')' in line " + str(inputlist[0][1])
                        return(0)
                else:
                    return(0)
            else:
                error = "Invalid Syntax - expected '(' in line " + str(inputlist[0][1])
                return(0)
        elif inputlist[0][0]=='while':
            inputlist.pop(0)
            if condicao():
                if inputlist[0][0]=='do':
                    inputlist.pop(0)
                    if comandos():
                        if inputlist[0][0]=='$':
                            inputlist.pop(0)
                            return(1)
                        else:
                            error = "Invalid Syntax - expected '$' in line " + str(inputlist[0][1])
                            return(0)
                    else:
                        return(0)
                else:
                    error = "Invalid Syntax - expected 'do' in line " + str(inputlist[0][1])
                    return(0)
            else:
                return(0)
        elif inputlist[0][0]=='if':
            inputlist.pop(0)
            if condicao():
                if inputlist[0][0]=='then':
                    inputlist.pop(0)
                    if comandos():
                        if pfalsa():
                            if inputlist[0][0]=='$':
                                inputlist.pop(0)
                                return(1)
                            else:
                                error = "Invalid Syntax - expected '$' in line " + str(inputlist[0][1])
                                return(0)
                        else:
                            return(0)
                    else:
                        return(0)
                else:
                    error = "Invalid Syntax - expected 'then' in line " + str(inputlist[0][1])
                    return(0)
            else:
                return(0)
        elif re.match('\w+', inputlist[0][0]) and re.match('[a-zA-Z]', inputlist[0][0][0]) and inputlist[0][0] not in preservada:
            inputlist.pop(0)
            if restoident():
                return(1)
            else:
                return(0)
        else:
            errorac.append("Invalid Syntax - expected 'read', 'write', 'while', 'if' or ident in line " + str(inputlist[0][1]))
            return(0)

    def restoident():
        global error

        if inputlist[0][0]==':=':
            inputlist.pop(0)
            if expressao():
                return(1)
            else:
                return(0)
        elif lista_arg():
            return(1)
        else:
            errorac.append("Invalid Syntax - expected ':=' in line " + str(inputlist[0][1]))
            return(0)

    def condicao():
        if expressao():
            if relacao():
                if expressao():
                    return(1)
                else:
                    return(0)
            else:
                return(0)
        else:
            return(0)

    def relacao():
        global error

        if inputlist[0][0]=='=' or inputlist[0][0]=='<>' or inputlist[0][0]=='>=' or inputlist[0][0]=='<=' or inputlist[0][0]=='>' or inputlist[0][0]=='<':
            inputlist.pop(0)
            return(1)
        else:
            errorac.append("Invalid Syntax - expected '=', '<>', '>=', '<=', '>' or '<' in line " + str(inputlist[0][1]))
            return(0)

    def expressao():
        if termo():
            if outros_termos():
                return(1)
            else:
                return(0)
        else:
            return(0)

    def op_un():
        global error

        if inputlist[0][0]=='+' or inputlist[0][0]=='-':
            inputlist.pop(0)
            return(1)
        elif error!=None:
            return(0)
        else:
            return(1)

    def outros_termos():
        global error

        if op_ad():
            if termo():
                if outros_termos():
                    return(1)
                else:
                    return(0)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def op_ad():
        global error

        if inputlist[0][0]=='+' or inputlist[0][0]=='-':
            inputlist.pop(0)
            return(1)
        else:
            errorac.append("Invalid Syntax - expected '+' or '-' in line " + str(inputlist[0][1]))
            return(0)

    def termo():
        if op_un():
            if fator():
                if mais_fatores():
                    return(1)
                else:
                    return(0)
            else:
                return(0)
        else:
            return(0)

    def mais_fatores():
        global error

        if op_mul():
            if fator():
                if mais_fatores():
                    return(1)
                else:
                    return(0)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            return(1)

    def op_mul():
        global error

        if inputlist[0][0]=='*' or inputlist[0][0]=='/':
            inputlist.pop(0)
            return(1)
        else:
            errorac.append("Invalid Syntax - expected '*' or '/' in line " + str(inputlist[0][1]))
            return(0)

    def fator():
        global error

        if re.match('\w+', inputlist[0][0]) and re.match('[a-zA-Z]', inputlist[0][0][0]) and inputlist[0][0] not in preservada:
            inputlist.pop(0)
            return(1)
        elif re.match('\d+.\d+', inputlist[0][0]):
            inputlist.pop(0)
            return(1)
        elif re.match('\d+', inputlist[0][0]):
            inputlist.pop(0)
            return(1)
        elif inputlist[0][0]=='(':
            inputlist.pop(0)
            if expressao():
                if inputlist[0][0]==')':
                    inputlist.pop(0)
                    return(1)
                else:
                    error = "Invalid Syntax - expected ')' in line " + str(inputlist[0][1])
                    return(0)
            else:
                return(0)
        else:
            errorac.append("Invalid Syntax - expected ident, integer, real or '(' in line " + str(inputlist[0][1]))
            return(0)


    try:
        if programa():
            print('Syntax Accepted, well done!\n')
            return(1)
        else:
            print(error)
            return(0)
    except:
        error = "Invalid Syntax - Not enough arguments"
        print(error)
        return(0)


inputlist = []
preservada = []
error = None

txt = open('test.txt', 'r')
brutecode = txt.read()
txt.close

val = 0

val = lexiconanal(brutecode)
#print(inputlist)
if val==1:
    val = syntaxanal()
    #print(inputlist)


