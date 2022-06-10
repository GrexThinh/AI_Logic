def readData(filename):
    with open(filename, 'r') as f:
        data = [s.strip() for s in f.readlines()]

    alpha=data[0]
    data.remove(data[0])
    data.remove(data[0])
    KB=data

    for i in range(0, len(KB)):
        KB[i] = KB[i].replace('OR', '')

    return alpha, KB

def checkLiteralOpposite(l1, l2):
    if l1[0]=='-' and l1[1]==l2[0]: return True
    elif l2[0]=='-' and l2[1]==l1[0]: return True
    else: return False

def checkDuplicate(clause):
    i=0
    n=len(clause)
    while i<n:
        check=False
        for j in range(i+1,n):
            if clause[i]==clause[j]:
                del clause[j]
                check=True
                break
        if check==True:
            i=0
            n-=1
        else: i+=1
    return clause

def makeNegativeLiteral(l):
    if l[0]=='-':
        return l[1]
    elif l[0]!='-':
        return '-'+l[0]

def insertLiteralToKB(alpha, KB):
    if len(alpha)==1 or len(alpha)==2:
        KB.append(makeNegativeLiteral(alpha))
    else:
        alpha=alpha.replace('OR','')
        s=alpha.split()
        for i in range(len(s)):
            s[i]=makeNegativeLiteral(s[i])
            KB.append(s[i])
    KB=checkDuplicate(KB)
    return KB

def sorter(elem):
    if len(elem)==2: return elem[1]
    else: return elem[0]

def solveKB(KB):
    new_literals=[]
    original_len=len(KB)
    checkEntail=False
    for i in range(0, len(KB)):
        for j in range(i+1,len(KB)):
            s=KB[i]+' '+KB[j]
            s=s.split()
            n=len(s)
            k=0
            count=0
            while k<n:
                check=False
                for m in range(k+1, n):
                    if checkLiteralOpposite(s[k],s[m])==True:
                        del s[m]
                        del s[k]
                        check=True
                        count+=1
                        n -= 2
                        break
                if check==True:
                    k=0
                else:
                    k+=1
            if count==1:
                s=sorted(s, key=sorter)
                res=[]
                if (len(s)==1):
                    res=s
                else:
                    s = checkDuplicate(s)
                    cls=''
                    for lit in range(len(s)):
                        cls+=s[lit]
                        if lit!=len(s)-1: cls+='  '
                    if cls=='':
                        cls='{}'
                        checkEntail=True
                    res.append(cls)
                new_literals.extend(res)

    KB.extend(new_literals)
    KB = checkDuplicate(KB)

    checkNewKB=False
    if (original_len<len(KB)): checkNewKB=True

    count=len(KB)-original_len

    new_cls=[]
    for cls in range(original_len, len(KB)):
        new_cls.append(KB[cls])

    return checkNewKB, checkEntail, count, KB, new_cls

def PL_RESOLUTION(lst_KB, fileout):
    checkNewKB, checkEntail, count, new_KB, new_cls=solveKB(lst_KB)
    fileout.write(str(count))
    fileout.write('\n')
    for i in range(len(new_cls)):
        new_cls[i]=new_cls[i].replace('  ',' OR ')
        fileout.write(new_cls[i])
        fileout.write('\n')
    if (checkEntail==True):
        fileout.write('YES')
        return True
    elif (checkNewKB==False and checkEntail==False):
        fileout.write('NO')
        return False
    else: return PL_RESOLUTION(new_KB,fileout)
