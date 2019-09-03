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

def lexiconanal(brutecode,inputlist,pile):
    import nltk
    import re
    
    mktoken = nltk.WordPunctTokenizer()
    termos = mktoken.tokenize(brutecode)
    print(" ============== \n Lista de Tokens \n =================")
    preservada = {'if', 'then', 'while', 'do', 'write', 'read', 'else', 'begin', 'end', 'var', 'real', 'integer', 'procedure'}
    ssimples = {'(', ')', '*', '/', '+', '-', '>', '<', '$', ';', ':', ',', '.', '='}
    tratar = {');'}
    sduplo = {'<>', '>=', '<=', ':='}
    com1 = False
    com2 = False
    numero = None
    numero_real = None
    check_line_token(brutecode,termos)
    for i,line in termos:    
        if com1 == True or com2 == True:
            if i == '*/':
                com1 = False
                print(i + ', Comentário')
            elif i == '}':
                com2 = False
                print(i + ', Comentário')
            else:
                print(i + ', Comentário')
        else:
            if numero!=None and numero_real==None and i!='.':
                print(i + ',  Numero Inteiro')
                numero = None
            if numero == None and numero_real == None:
                if i == '/*':
                    com1 = True
                    print(i + ', Comentário')
                elif i == '{':
                    com2 = True
                    print(i + ', Comentário')
                elif i in preservada:
                    print(i + ', Palavra Reservada')
                elif i in tratar:
                    print(i[0] + ', Simbolo Simples')
                    print(i[1] + ', Simbolo Simples')
                elif i in ssimples:
                    print(i + ', Simbolo Simples')
                elif i in sduplo:
                    print(i + ', Simbolo Duplo')    
                elif re.match('\w+', i) and re.match('[a-zA-Z]', i[0]):
                    print(i + ',  Identificador')
                elif i.isdigit():
                    numero = i
                else:
                    print(str(i) + ',  token inválido na linha: ' + str(line))
                    return(0)
            elif numero_real == None and i=='.':
                numero_real = str(numero)+i
            elif numero_real!=None and i.isdigit():
                numero_real = numero_real+str(i)
                print(numero_real + ',  Numero Real')
                numero = None
                numero_real = None               
            else:
                print(numero_real + ',  token inválido na linha: ' + str(line))
                return(0)
        pile.append(i)
    pile.append('n')
    print('Accepted Lexicon')
    return (1)

inputlist = []
pile = []

txt = open('test.txt', 'r')
brutecode = txt.read()
val = 0

val = lexiconanal(brutecode,inputlist,pile)

print("\n\n PILE STARTS HERE \n")
print (pile)

txt.close
