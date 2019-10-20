import sys
import re
import operator
from collections import OrderedDict
from collections import defaultdict
import json


wordcount={}
classes=OrderedDict()
totalmsg=0
sum=OrderedDict()
count=0
wavg=defaultdict(dict)

for line in open(str(sys.argv[1]), "r", errors='ignore'):
    wavg=json.loads(line)

i=0



for line in sys.stdin:
    line=line.rstrip('\n')
    l=line.split()
    actualclass=l[0]
    t=l[1:]
    for k,v in wavg.items():
        sum[str(k)]=0
        for word in t:
            wavg[str(k)].setdefault(word, 0)

            sum[str(k)]=sum[str(k)]+wavg[str(k)][word]
    value=list(sum.values())
    key=list(sum.keys())
    predclass=key[value.index(max(value))]

    if(sum[list(wavg.keys())[0]]>=sum[predclass]):
        predclass=list(wavg.keys())[0]
    
    sys.stdout.write(predclass+"\n")
        
