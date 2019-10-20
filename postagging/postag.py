import sys
import re
import operator
from collections import OrderedDict
from collections import defaultdict
import json

def preprocesor(sentence):
    s=[]

    line=sentence.rstrip('\n')
    l=line.split()
    c=0
    for words in l:
        if c==0:
            prevw='BOS/BOS'
        else:
            prevw=l[c-1]
        if c==len(l)-1:
            nextw='EOS/EOS'
        else:
            nextw=l[c+1]
        '''
        prevwordtemp=prevw.split('/')
        prevword=prevw.split('/')[:-1]
        prev='/'.join(prevword)
        
        nextwordtemp=nextw.split('/')
        nextword=nextw.split('/')[:-1]
        next='/'.join(nextword)
        
        currentwordtemp=words.split('/')
        currentword=words.split('/')[:-1]
        current='/'.join(currentword)
        '''
        prevword=prevw.split('/')
        nextword=nextw.split('/')
        currentword=words.split('/')

        charac=''
#        current=currentword[0]
        if(currentword[0].islower()):
            charac='a'
        if(currentword[0].isupper()):
            charac='A'
        if (re.match('^[0-9]+$',currentword[0])):
            charac='9'
        if (re.match('^[A-Z]+[a-z]+$',currentword[0])):
            charac='Aa'
        if (re.match('^[A-Z]+[0-9]+$',currentword[0])):
            charac='A9'
        if (re.match('^[a-z]+[A-Z]+$',currentword[0])):
            charac='aA'
        if (re.match('^[a-z]+[0-9]+$',currentword[0])):
            charac='a9'
        if (re.match('^[0-9]+[A-Z]+$',currentword[0])):
            charac='9A'
        if (re.match('^[0-9]+[a-z]+$',currentword[0])):
            charac='9a'
        
        if (re.match('^[A-Z]+[a-z]+[0-9]+$',currentword[0])):
            charac='Aa9'
        if (re.match('^[A-Z]+[0-9]+[a-z]+$',currentword[0])):
            charac='A9a'
        if (re.match('^[a-z]+[A-Z]+[0-9]+$',currentword[0])):
            charac='aA9'
        if (re.match('^[a-z]+[0-9]+[A-Z]+$',currentword[0])):
            charac='a9A'
        if (re.match('^[0-9]+[A-Z]+[a-z]+$',currentword[0])):
            charac='9Aa'
        if (re.match('^[0-9]+[a-z]+[A-Z]+$',currentword[0])):
            charac='9aA'
        
        s.append('prev:'+prevword[0]+" current:"+currentword[0]+" next:"+nextword[0]+" suffix3:"+currentword[0][-3:]+" suffix2:"+currentword[0][-2:]+" case:"+charac)

        c=c+1
    return [s]

wordcount={}
classes=OrderedDict()
totalmsg=0
sum=OrderedDict()
count=0
wavg=defaultdict(dict)

for line in open(str(sys.argv[1]), "r", errors='ignore'):
    wavg=json.loads(line)

i=0

s=[]


for sentence in sys.stdin:
    sent=sentence.split()
    s=preprocesor(sentence)
#    print(s)
    wc=0
    for line in s[0]:
#        print(line)
#        print()
        l=line.split()
        t=l[0:]
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
        sys.stdout.write(sent[wc]+"/"+predclass+" ")
        sys.stdout.flush()
        
        wc=wc+1
    print('')