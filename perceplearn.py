import sys
import re
import operator
from collections import OrderedDict
from collections import defaultdict
from random import shuffle
import random
import json

wordcount={}
classes=OrderedDict()
totalmsg=0
sum=OrderedDict()

for line in open(str(sys.argv[1]), "r",  errors='ignore'):
    line=line.rstrip('\n')
    l=line.split()
    t=l[1:]
    classes[l[0]]='true'

defclass = list(classes.keys())

w=defaultdict(dict)
wavg=defaultdict(dict)
c=1

for line in open(str(sys.argv[1]), "r", errors='ignore'):
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

with open(str(sys.argv[1]),  errors='ignore') as f:
    lines = f.readlines()

for i in range(25): 
    count=0
    ecount=0
    random.shuffle(lines)
#    print("Iteration"+str(i)+"\n")
    for line in lines:
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
