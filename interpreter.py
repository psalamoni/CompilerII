def interpreter(pile):
    import re
    D = []

    for i in range(len(pile)):
        if re.match('\d+.\d+', pile[i]) or re.match('\d+', pile[i]):
            pile[i] = float(pile[i])
        D.append(pile[i])
    
    s=-1

    for i in range(len(pile)):
        current = pile[i]
        if current[:4]=="CRCT":
            k = int(current[5:])
            s=s+1
            D[s] = k
        elif current[:4]=="CRVL":
            n = int(current[5:])
            if D[n] == None:
                print("Index ["+str(n)+"] var not assigned")
                return (0)
            s=s+1
            D[s] = D[n]
        elif current=="SOMA":
            D[s-1]= D[s-1] + D[s]
            s = s-1
        elif current=="SUBT":
            D[s-1] = D[s-1] - D[s]
            s = s-1
        elif current=="MULT":
            D[s-1]= D[s-1] * D[s]
            s = s-1
        elif current=="DIVI":
            D[s-1]= D[s-1] / D[s]
            s = s-1
        elif current=="INVE":
            D[s]= -D[s]
        elif current=="CPME":
            if D[s-1] < D[s]:
                D[s-1]= 1
            else:
                D[s-1]= 0
            s= s-1
        elif current=="CPMA":
            if D[s-1] > D[s]:
                D[s-1]= 1
            else:
                D[s-1]= 0
            s= s-1
        elif current=="CPIG":
            if D[s-1] == D[s]:
                D[s-1]= 1
            else:
                D[s-1]= 0
            s= s-1
        elif current=="CDES":
            if D[s-1] != D[s]:
                D[s-1]= 1
            else:
                D[s-1]= 0
            s= s-1
        elif current=="CPMI":
            if D[s-1] <= D[s]:
                D[s-1]= 1
            else:
                D[s-1]= 0
            s= s-1
        elif current=="CMAI":
            if D[s-1] >= D[s]:
                D[s-1]= 1
            else:
                D[s-1]= 0
            s= s-1
        elif current[:4]=="ARMZ":
            n = int(current[5:])
            D[n] = D[s]
            s=s-1
        elif current[:4]=="DSVI":
            p = int(current[5:])
            i=p
        elif current[:4]=="DSVF":
            p = int(current[5:])
            if D[s]==0:
                i= p
            s=s-1
        elif current=="LEIT":
            s= s+1
            print ("\nType input value:\n")
            D[s] = int(input())
        elif current=="IMPR":
            print (D[s])
            s= s-1
        elif current[:4]=="ALME":
            m = int(current[5:])
            D[s]=None
            s=s+m
        elif current[:current.find("")]=="PARAM":
            n = int(current[current.find("")+1:])
            s=s+1
            D[s]= D[n]
        elif current[:current.find("")]=="PUSHER":
            e = int(current[current.find("")+1:])
            s=s+1
            D[s]= e
        elif current[:4]=="CHPR":
            p = int(current[5:])
            i=p
        elif current[:4]=="DESM":
            m = int(current[5:])
            s = s-m
        elif current=="RTPR":
            i = D[s]
            s= s-1
        

    return (1)    
       


