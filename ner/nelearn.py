import sys
import re
import operator
from collections import OrderedDict
from collections import defaultdict
from random import shuffle
import random
import json

def preprocessing():
    s=[]
    for line in open(str(sys.argv[1]), "r", errors='ignore'):
        line=line.rstrip('\n')
        l=line.split()
        c=0
        for words in l:
            if c==0:
                prevw='BOS/BOS/BOS'
            else:
                prevw=l[c-1]
            if c==len(l)-1:
                nextw='EOS/EOS/EOS'
            else:
                nextw=l[c+1]
            prevwordtemp=prevw.split('/')
            prevword=prevw.split('/')[:-2]
            prev='/'.join(prevword)
            
            nextwordtemp=nextw.split('/')
            nextword=nextw.split('/')[:-2]
            next='/'.join(nextword)
            
            currentwordtemp=words.split('/')
            currentword=words.split('/')[:-2]
            current='/'.join(currentword)

            charac=''
    #        current=currentword[0]
            if(current.islower()):
                charac='a'
            if(current.isupper()):
                charac='A'
            if (re.match('^[0-9]+$',current)):
                charac='9'
            if (re.match('^[A-Z]+[a-z]+$',current)):
                charac='Aa'
            if (re.match('^[A-Z]+[0-9]+$',current)):
                charac='A9'
            if (re.match('^[a-z]+[A-Z]+$',current)):
                charac='aA'
            if (re.match('^[a-z]+[0-9]+$',current)):
                charac='a9'
            if (re.match('^[0-9]+[A-Z]+$',current)):
                charac='9A'
            if (re.match('^[0-9]+[a-z]+$',current)):
                charac='9a'
            
            if (re.match('^[A-Z]+[a-z]+[0-9]+$',current)):
                charac='Aa9'
            if (re.match('^[A-Z]+[0-9]+[a-z]+$',current)):
                charac='A9a'
            if (re.match('^[a-z]+[A-Z]+[0-9]+$',current)):
                charac='aA9'
            if (re.match('^[a-z]+[0-9]+[A-Z]+$',current)):
                charac='a9A'
            if (re.match('^[0-9]+[A-Z]+[a-z]+$',current)):
                charac='9Aa'
            if (re.match('^[0-9]+[a-z]+[A-Z]+$',current)):
                charac='9aA'

#            s.append(currentword[2]+' prev:'+prevword[0]+" current:"+currentword[0]+" next:"+nextword[0]+" prevtag:"+prevword[1]+" currenttag:"+currentword[1]+" nexttag:"+nextword[1])
            s.append(currentwordtemp[-1]+' prev:'+prev+" current:"+current+" next:"+next+" prevtag:"+prevwordtemp[-2]+" currenttag:"+currentwordtemp[-2]+" nexttag:"+nextwordtemp[-2]+" suffix3:"+current[-3:]+" suffix2:"+current[-2:]+" case:"+charac)
            c=c+1
    return [s]


wordcount={}
classes=OrderedDict()
totalmsg=0
sum=OrderedDict()

s=[]
s=preprocessing()

#print(s[0][0])

for line in s[0]:
    line=line.rstrip('\n')
    l=line.split()
    t=l[1:]
    classes[l[0]]='true'

defclass = list(classes.keys())

w=defaultdict(dict)
wavg=defaultdict(dict)
c=1

for line in s[0]:
    line=line.rstrip('\n')
    l=line.split()
    t=l[1:]
    for k,v in classes.items():
        for word in t:
            w[str(k)][word]=0
            wavg[str(k)][word]=0
            
i=0

ecount=0
count=0
error=0
preverror=0

#with open(str(sys.argv[1]),  errors='ignore') as f:
#    lines = f.readlines()

for i in range(25): 
    count=0
    ecount=0
    random.shuffle(s[0])
#    print("Iteration"+str(i)+"\n")
    for line in s[0]:
        count=count+1
        line=line.rstrip('\n')
        l=line.split()
        t=l[1:]
        for k,v in classes.items():
            sum[str(k)]=0
            for word in t:
                sum[str(k)]=sum[str(k)]+w[str(k)][word]
        
        value=list(sum.values())
        key=list(sum.keys())
        predclass=key[value.index(max(value))]
                    
                    
        if(sum[defclass[0]]>=sum[predclass]):
            predclass=defclass[0]
        if l[0]!=predclass:
            ecount=ecount+1
            for word1 in t: #set(t):
                wavg[l[0]][word1]=wavg[l[0]][word1]+c
                wavg[predclass][word1]=wavg[predclass][word1]-c
                w[l[0]][word1]=w[l[0]][word1]+1
                w[predclass][word1]=w[predclass][word1]-1
        
        c=c+1
#    print(str(ecount)+" "+str(count))
#    error=float(ecount)/float(count)
#    delta=preverror-error
#    preverror=error
#    print("Error: "+str(error))        
#    print("Delta Error: "+str(delta))        
        
fo=open(str(sys.argv[2]), "a",  errors='ignore')

for k,v in classes.items():
    for l,m in wavg[str(k)].items():
        wavg[str(k)][str(l)]=float(w[str(k)][str(l)])-(float(wavg[str(k)][str(l)])/c)
fo.write(json.dumps(wavg))


fo.close()
