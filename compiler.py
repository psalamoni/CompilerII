from interpreter import interpreter

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

def createtable(identtb):
    global tokenstb
    global error

    if tokenstb.get(identtb) == None:
        tokenstb.update({identtb:{}})
        return(1)
    else:
        error = "Ident already in use, please define another ident in line: " + str(inputlist[0][1])
        return (0)

def inserttoken(token,request):
    global tokenstb
    global error

    token_scope = tokenstb.get(token[0])

    for tkn in token[2:]:
        if request:
            if token_scope.get(0) != None:
                new_token = token_scope.get(0)
                new_token.append(tkn[0])
                token_scope.update({0: new_token})
            else:
                token_scope.update({0: [tkn[0]]})
        if token_scope.get(tkn[0]) == None:
            token_scope.update({tkn[0]: token[1]})
        else:
            error = "Ident already in use, please define another ident in line: " + str(token[-1][1])
            return (0)
    return(1)

def valtype(token):
    global error
    
    for i in range(len(token[2:])):
        i = i+1
        if token[i]!=token[i+1]:
            error = "Ident's type doesn't match - "+token[i]+" | "+token[i+1]+" - in line: "+str(inputlist[0][1])
            return (0)
    return(1)

def valproc(token):
    global tokenstb
    global error

    token_scope = tokenstb.get(token[0])
    
    if len(token_scope.get(0)) != len(token)-1:
        error = "Invalid number of arguments in line: "+str(inputlist[0][1])
        return (0)
    for i in range(len(token_scope.get(0))):
        requirements = token_scope.get(0)
        if gettype([token[0],requirements[i]]) != gettype([token[0],token[i+1][0]]):
            error = "Parameter type doesn't match in procedure '"+token[0]+"' - "+ gettype([token[0],requirements[i]]) +" | "+ gettype([token[0],token[i+1][0]]) +" - in line: "+str(inputlist[0][1])
            return (0)
    return (1)

def gettype(token):
    global tokenstb
    global error

    token_scope = tokenstb.get(token[0])
    token_global = tokenstb.get(0)

    if token_scope.get(token[-1][0]) != None:
        return(token_scope.get(token[-1][0]))
    elif token_global.get(token[-1][0]) != None:
        return(token_global.get(token[-1][0]))
    else:
        error = "Ident '" + token[-1][0] + "' not declared, please define var before use it. Line: " + str(token[-1][1])
        return (0)    

def loadvar(var):
    global tokenstb
    global error
    global loaded
    
    token_scope = tokenstb.get(token[0])
    token_global = tokenstb.get(0)

    if token_scope.get(var[0]) != None:
        loaded.append(var[0])
        return (1)
    elif token_global.get(var[0]) != None:
        loaded.append(var[0])
        return (1)
    else:
        error = "Ident '" + var[0] + "' not declared, please define var before use it. Line: " + str(var[1])
        return (0)

def searchvarid(var):
    for i in range(len(datapile)):
        if datapile[i]==var:
            return i

def searchprocid(var):
    for i in range(len(datapile)):
        if datapile[i][0]==0:
            if datapile[i][2]==var:
                return datapile[i][1]

def correctprocret():
    for i in range(len(datapile)):
        if datapile[i][0]==0:
            datapile[i]="ret*"

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
    sduplo = {'<>', '>=', '<=', ':=', '/*', '*/'}
    com1 = False
    com2 = False
    numero = None
    numero_real = None
    check_line_token(brutecode,termos)
    temp = []

    for [x,termo] in enumerate(termos):
        i = termo[0]
        line = termo[1]

        if not re.match('\w+', i):
            if i not in ssimples and i not in sduplo:
                d=0
                while d<len(i):
                    if d<len(i)-1:
                        if (i[d]+i[d+1]) in sduplo:
                            temp.append([i[d]+i[d+1],line])
                            d+=2
                        else:
                            temp.append([i[d],line])
                            d+=1
                    else:
                        temp.append([i[d],line])
                        d+=1
            else:
                temp.append(termos[x])
        else:
            temp.append(termos[x])
    termos = temp

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
                inputlist.append([numero,line])
                numero = None
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
                elif i[0] == '(':
                    #print(i[0] + ', Simbolo Simples')
                    inputlist.append([i[0],line])
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
    global token
    global hypocode
    global datapile
    errorac = []
    localvarnum = []

    def programa():
        global error
        global token

        if inputlist[0][0]=='program':
            inputlist.pop(0)
            hypocode.append("INPP")
            if re.match('\w+', inputlist[0][0]) and re.match('[a-zA-Z]', inputlist[0][0][0]) and inputlist[0][0] not in preservada:
                if createtable(0):
                    inputlist.pop(0)
                    if corpo():
                        if inputlist[0][0]=='.':
                            inputlist.pop(0)
                            hypocode.append("PARA")
                            return(1)
                        else:
                            error = "Invalid Syntax - expected '.' in line " + str(inputlist[0][1])
                            return(0)
                    else:
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
                        correctprocret()
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
        global token

        if inputlist[0][0]=='var':
            inputlist.pop(0)
            if variaveis():
                if inputlist[0][0]==':':
                    inputlist.pop(0)
                    if tipo_var():
                        if inserttoken(token,False):
                            token = [token[0]]
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
        else:
            errorac.append("Invalid Syntax - expected 'var' in line " + str(inputlist[0][1]))
            return(0)

    def tipo_var():
        global error

        if inputlist[0][0]=='real' or inputlist[0][0]=='integer':
            token.insert(1,inputlist[0][0])
            inputlist.pop(0)
            return(1)
        else:
            errorac.append("Invalid Syntax - expected 'real' or 'integer' in line " + str(inputlist[0][1]))
            return(0)

    def variaveis():
        global error

        if re.match('\w+', inputlist[0][0]) and re.match('[a-zA-Z]', inputlist[0][0][0]) and inputlist[0][0] not in preservada:
            token.append(inputlist[0])
            datapile.append(inputlist[0][0])
            hypocode.append("ALME 1")
            if len(localvarnum)>0:
                localvarnum.append(inputlist[0][0])
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
        global token

        if inputlist[0][0]=='procedure':
            hypocode.append("ALME 1")
            localvarnum.append(len(hypocode))
            hypocode.append("savespace")
            inputlist.pop(0)
            if re.match('\w+', inputlist[0][0]) and re.match('[a-zA-Z]', inputlist[0][0][0]) and inputlist[0][0] not in preservada:
                datapile.append([0,len(hypocode),inputlist[0][0]])
                if createtable(inputlist[0][0]):
                    token = [inputlist[0][0]]
                    inputlist.pop(0)
                    if parametros():
                        if corpo_p():
                            return(1)
                        else:
                            return(0)
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
        global token

        if variaveis():
            if inputlist[0][0]==':':
                inputlist.pop(0)
                if tipo_var():
                    if inserttoken(token,True):
                        token = [token[0]]
                        if mais_par():
                            return(1)
                        else:
                            return(0)
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
        global token

        if dc_loc():
            if inputlist[0][0]=='begin':
                inputlist.pop(0)
                if comandos():
                    if inputlist[0][0]=='end':
                        hypocode.append("DESM "+str(len(localvarnum)-1))
                        hypocode.append("RTPR")
                        hypocode[localvarnum[0]] = "DSVI "+str(len(hypocode))
                        localvarnum.clear()
                        token = [0]
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
        global token
        global hypocode

        program = hypocode.pop()
        localvarnum.append(len(hypocode))
        hypocode.append("savespace")
        if inputlist[0][0]=='(':
            token = [token[-1]]
            inputlist.pop(0)
            if argumentos():
                if inputlist[0][0]==')':
                    if valproc(token):
                        inputlist.pop(0)
                        hypocode.append("CHPR "+str(searchprocid(program)))
                        hypocode[localvarnum[0]] = "PUSHER "+str(len(hypocode))
                        return(1)
                    else:
                        return(0)
                else:
                    error = "Invalid Syntax - expected ')' in line " + str(inputlist[0][1])
                    return(0)
            else:
                return(0)
        elif error!=None:
            return(0)
        else:
            hypocode.append("CHPR "+str(searchprocid(program)))
            return(1)

    def argumentos():
        global error

        if re.match('\w+', inputlist[0][0]) and re.match('[a-zA-Z]', inputlist[0][0][0]) and inputlist[0][0] not in preservada:
            token.append(inputlist[0])
            hypocode.append("PARAM "+str(searchvarid(inputlist[0][0])))
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
        global token
        global hypocode
        process = []
        
        token = [token[0]]
        if inputlist[0][0]=='read':
            inputlist.pop(0)
            if inputlist[0][0]=='(':
                inputlist.pop(0)
                if variaveis():
                    if loadvar(token.pop()):
                        # Se existe variável
                        if inputlist[0][0]==')':
                            while hypocode[-1]=="ALME 1":
                                process.append("ARMZ "+str(searchvarid(datapile.pop())))
                                process.append("LEIT")
                                hypocode.pop()
                            process.reverse()
                            hypocode = hypocode[:]+process[:]
                            process.clear()
                            inputlist.pop(0)
                            return(1)
                        else:
                            error = "Invalid Syntax - expected ')' in line " + str(inputlist[0][1])
                            return(0)
                    else:
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
                    # Se existe variável
                    if inputlist[0][0]==')':
                        while hypocode[-1]=="ALME 1":
                            process.append("IMPR")
                            process.append("CRVL "+str(searchvarid(datapile.pop())))
                            hypocode.pop()
                        process.reverse()
                        hypocode = hypocode[:]+process[:]
                        process.clear()
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
            localvarnum.append(len(hypocode))
            inputlist.pop(0)
            if condicao():
                if inputlist[0][0]=='do':
                    localvarnum.append(len(hypocode))
                    hypocode.append("savespace")
                    inputlist.pop(0)
                    comandos()
                    if inputlist[0][0]=='$':
                        hypocode.append("DSVI "+str(localvarnum[0]+1))
                        hypocode[localvarnum[1]] = "DSVF "+str(len(hypocode))
                        localvarnum.clear()
                        inputlist.pop(0)
                        return(1)
                    else:
                        error = "Invalid Syntax - expected '$' in line " + str(inputlist[0][1])
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
                    localvarnum.append(len(hypocode))
                    hypocode.append("savespace")
                    inputlist.pop(0)
                    if comandos():
                        hypocode[localvarnum[0]] = "DSVF "+str(len(hypocode)+1)
                        localvarnum.clear()
                        localvarnum.append(len(hypocode))
                        hypocode.append("savespace")
                        if pfalsa():
                            hypocode[localvarnum[0]] = "DSVI "+str(len(hypocode))
                            localvarnum.clear()
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
            hypocode.append(inputlist[0][0])
            token.append(inputlist[0][0])
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
        global token
        global hypocode

        if inputlist[0][0]==':=':
            varid = searchvarid(hypocode.pop())
            hypocode.append("ARMZ "+str(varid))
            token[-1] = gettype(token)
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
                    hypocode.append(localvarnum.pop())
                    localvarnum.clear()
                    localvarnum.append(len(hypocode))
                    return(1)
                else:
                    return(0)
            else:
                return(0)
        else:
            return(0)

    def relacao():
        global error

        if inputlist[0][0]=='=':
            localvarnum.append("CPIG")
            inputlist.pop(0)
            return(1)
        elif inputlist[0][0]=='<>':
            localvarnum.append("CDES")
            inputlist.pop(0)
            return(1)
        elif inputlist[0][0]=='>=':
            localvarnum.append("CMAI")
            inputlist.pop(0)
            return(1)
        elif inputlist[0][0]=='<=':
            localvarnum.append("CPMI")
            inputlist.pop(0)
            return(1)
        elif inputlist[0][0]=='>':
            localvarnum.append("CPMA")
            inputlist.pop(0)
            return(1)
        elif inputlist[0][0]=='<':
            localvarnum.append("CPME")
            inputlist.pop(0)
            return(1)
        else:
            errorac.append("Invalid Syntax - expected '=', '<>', '>=', '<=', '>' or '<' in line " + str(inputlist[0][1]))
            return(0)

    def expressao():
        global token

        if termo():
            if outros_termos():
                return(1)
            else:
                return(0)
        else:
            return(0)

    def op_un():
        global error
        operators = ["ARMZ"]

        if inputlist[0][0]=='+':
            inputlist.pop(0)
            return(1)
        elif inputlist[0][0]=='-':
            inputlist.pop(0)
            if hypocode[-1][:4] in operators:
                if hypocode[-2]=="SOMA":
                    temp = hypocode.pop()
                    hypocode.pop()
                    hypocode.append("SUBT")
                    hypocode.append(temp)
                elif hypocode[-2]=="SUBT":
                    temp = hypocode.pop()
                    hypocode.pop()
                    hypocode.append("SOMA")
                    hypocode.append(temp)
                else:
                    temp = hypocode.pop()
                    hypocode.append("INVE")
                    hypocode.append(temp)
            else:
                if hypocode[-1]=="SOMA":
                    hypocode.pop()
                    hypocode.append("SUBT")
                elif hypocode[-1]=="SUBT":
                    hypocode.pop()
                    hypocode.append("SOMA")
                else:
                    hypocode.append("INVE")
            return(1)
        elif error!=None:
            return(0)
        else:
            return(1)

    def outros_termos():
        global error
        global token

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
            if valtype(token):
                token = [token[0]]
                return(1)
            else:
                return(0)

    def op_ad():
        global error
        operators = ["ARMZ"]

        if inputlist[0][0]=='+':
            inputlist.pop(0)
            if hypocode[-1][:4] in operators:
                temp = hypocode.pop()
                hypocode.append("SOMA")
                hypocode.append(temp)
            else:
                hypocode.append("SOMA")
            return(1)
        elif inputlist[0][0]=='-':
            inputlist.pop(0)
            if hypocode[-1][:4] in operators:
                temp = hypocode.pop()
                hypocode.append("SUBT")
                hypocode.append(temp)
            else:
                hypocode.append("SUBT")
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

        if inputlist[0][0]=='*':
            inputlist.pop(0)
            hypocode.append("MULT")
            return(1)
        elif inputlist[0][0]=='/':
            inputlist.pop(0)
            hypocode.append("DIVI")
            return(1)
        else:
            errorac.append("Invalid Syntax - expected '*' or '/' in line " + str(inputlist[0][1]))
            return(0)

    def fator():
        global error
        global hypocode
        operators = ["INVE","SOMA","SUBT","MULT","DIVI"]
        opend = ["ARMZ"]

        if re.match('\w+', inputlist[0][0]) and re.match('[a-zA-Z]', inputlist[0][0][0]) and inputlist[0][0] not in preservada:
            token.append(inputlist[0])
            token[-1] = gettype(token)
            if hypocode[-1][:4] in opend:
                if hypocode[-2] in operators:
                    temp2 = hypocode.pop()
                    temp1 = hypocode.pop()
                    hypocode.append("CRVL "+str(searchvarid(inputlist[0][0])))
                    hypocode.append(temp1)
                    hypocode.append(temp2)
                else:
                    temp = hypocode.pop()
                    hypocode.append("CRVL "+str(searchvarid(inputlist[0][0])))
                    hypocode.append(temp)
            else:
                if hypocode[-1] in operators:
                    temp = hypocode.pop()
                    hypocode.append("CRVL "+str(searchvarid(inputlist[0][0])))
                    hypocode.append(temp)
                else:
                    hypocode.append("CRVL "+str(searchvarid(inputlist[0][0])))
            inputlist.pop(0)
            return(1)
        elif re.match('\d+.\d+', inputlist[0][0]):
            token.append('real')
            if hypocode[-1][:4] in opend:
                if hypocode[-2] in operators:
                    temp2 = hypocode.pop()
                    temp1 = hypocode.pop()
                    hypocode.append("CRCT "+inputlist[0][0])
                    hypocode.append(temp1)
                    hypocode.append(temp2)
                else:
                    temp = hypocode.pop()
                    hypocode.append("CRCT "+inputlist[0][0])
                    hypocode.append(temp)
            else:
                if hypocode[-1] in operators:
                    temp = hypocode.pop()
                    hypocode.append("CRCT "+inputlist[0][0])
                    hypocode.append(temp)
                else:
                    hypocode.append("CRCT "+inputlist[0][0])
            inputlist.pop(0)
            return(1)
        elif re.match('\d+', inputlist[0][0]):
            token.append('integer')
            if hypocode[-1][:4] in opend:
                if hypocode[-2] in operators:
                    temp2 = hypocode.pop()
                    temp1 = hypocode.pop()
                    hypocode.append("CRCT "+inputlist[0][0])
                    hypocode.append(temp1)
                    hypocode.append(temp2)
                else:
                    temp = hypocode.pop()
                    hypocode.append("CRCT "+inputlist[0][0])
                    hypocode.append(temp)
            else:
                if hypocode[-1] in operators:
                    temp = hypocode.pop()
                    hypocode.append("CRCT "+inputlist[0][0])
                    hypocode.append(temp)
                else:
                    hypocode.append("CRCT "+inputlist[0][0])
            inputlist.pop(0)
            return(1)
        elif inputlist[0][0]=='(':
            if hypocode[-1][:4] in opend:
                tempp2 = hypocode.pop()
                tempp1 = hypocode.pop()
                outside = hypocode[:]
                hypocode = ["",""]
            else:
                tempp1 = None
                tempp = hypocode.pop()
                outside = hypocode[:]
                hypocode = ["",""]
            inputlist.pop(0)
            if expressao():
                if inputlist[0][0]==')':
                    if tempp1 is not None :
                        hypocode = outside[:]+hypocode[2:]
                        hypocode.append(tempp1)
                        hypocode.append(tempp2)
                        tempp1=None
                    else:
                        hypocode = outside[:]+hypocode[2:]
                        hypocode.append(tempp)
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


    #try:
    if programa():
        print('Syntax Accepted, well done!\n')
        return(1)
    else:
        if error != None:
            print(error)
        else:
            print(errorac.pop())
        return(0)
    """except:
        error = "Invalid Syntax - Not enough arguments"
        print(error)
        return(0)"""


inputlist = []
preservada = []
token = [0]
loaded = []
tokenstb = {}
error = None
hypocode = []
datapile = []


txt = open('test.txt', 'r')
brutecode = txt.read()
txt.close

val = 0

val = lexiconanal(brutecode)

if val==1:
    val = syntaxanal()

if val==1:
    val = interpreter(hypocode)
    print ("EOF")



