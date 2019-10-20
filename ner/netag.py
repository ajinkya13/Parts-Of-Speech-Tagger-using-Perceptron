import sys
import re
import operator
from collections import OrderedDict
from collections import defaultdict
import json
import codecs

def preprocesor(sentence):
    s=[]

    line=sentence.rstrip('\n')
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
        prevword=prevw.split('/')[:-1]
        prev='/'.join(prevword)
        
        nextwordtemp=nextw.split('/')
        nextword=nextw.split('/')[:-1]
        next='/'.join(nextword)
        
        currentwordtemp=words.split('/')
        currentword=words.split('/')[:-1]
        current='/'.join(currentword)
#        print(prev+" "+next+" "+current)
#            s.append(currentword[2]+' prev:'+prevword[0]+" current:"+currentword[0]+" next:"+nextword[0]+" prevtag:"+prevword[1]+" currenttag:"+currentword[1]+" nexttag:"+nextword[1])
#        print('prev:'+prev+" current:"+current+" next:"+next+" prevtag:"+prevwordtemp[-1]+" currenttag:"+currentwordtemp[-1]+" nexttag:"+nextwordtemp[-1])

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

        s.append('prev:'+prev+" current:"+current+" next:"+next+" prevtag:"+prevwordtemp[-1]+" currenttag:"+currentwordtemp[-1]+" nexttag:"+nextwordtemp[-1]+" suffix3:"+current[-3:]+" suffix2:"+current[-2:]+" case:"+charac)
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
sys.stdin = codecs.getreader('utf8')(sys.stdin.detach(), errors='ignore')
for sentence in sys.stdin:
    sent=sentence.split()
    s=preprocesor(sentence)
    wc=0
    #print(s[0][0])
    #for i in range(3): 
    for line in s[0]:
    #    line=line.rstrip('\n')
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
    print()