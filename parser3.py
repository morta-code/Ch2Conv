#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
import re

def openf(filename): # Fájlbeolvasó, ami magába foglaja a hibakezelést.
    try:
        with codecs.open(filename,'r','utf-8') as f:
            return f.readlines() # Mindent berak egyszerre a memóriába. Nagy fájlokon nem szabad használni!!!
    except IOError:
        printerr(u"Nem sikerült megnyitni a fájlt: '" + filename.decode("utf-8") + u"' !")
        sys.exit(1)

def printout(text): # Kiíró függvény, ami magában foglalja az encode-olást.
    sys.stdout.write((text + u"\n").encode('utf-8'))

def printerr(text): # Kiíró függvény, ami magában foglalja az encode-olást.
    sys.stderr.write((text + u"\n").encode('utf-8'))

def felt(szo,x):
    pattern = re.compile(u'^.*[a-zA-ZíűáéúőóüöÍŰÁÉÚŐÓÜÖ]{4}.*$') # Egyáltalán van benne 4 betű egymás mellett. -> Különben nincs is nagyon mit elgépelni rajta.
    pattern2 = re.compile(u'^-[a-zA-ZíűáéúőóüöÍŰÁÉÚŐÓÜÖ]{1,4}$') # Ha úgy néz ki mint egy különálló toldalék akkor kuka.
    elso = u"[" + u"[".join(x.split(u"[")[1:]) == nyertes_tag	
    szoto = x.split(u"[")[0]	
    masodik = pattern.match(szoto)!=None and pattern2.match(szoto)==None
    szo_kozepe=szo[1:-1]
    szoto_kozepe=re.sub(u'-$',"",szoto[1:-1])
    harmadik = szo_kozepe.isupper() == szoto_kozepe.isupper() and szo_kozepe.islower() == szoto_kozepe.islower()
    return elso and masodik and harmadik

lines=openf(sys.argv[1])
from collections import defaultdict
lemmak=defaultdict(int)
lemmak2=defaultdict(int)
for l in lines:
    words=l.split()
    words_ki=[]
    for w in words:
        szo =            w.split(u"{{")[0]
        elemzesek_raw =  w.split(u"{{")[1].split(u"}}#")[0]
        spellcheck =bool(int(w.split(u"{{")[1].split(u"}}#")[1].split(u"#")[0]))
        szegedcheck=bool(int(w.split(u"{{")[1].split(u"}}#")[1].split(u"#")[1]))
        elmezesek_raw2=elemzesek_raw.split(u"||")
        if u"<" in elmezesek_raw2[0]:
            # Nem a 0. index az első humor elemzés -> Üres listát inicializálunk.
            humor_elemzes=[]
            # Guesser elemzések kigyűjtése.
            guesser_elemzes=elmezesek_raw2[0][1:].split(u">[")[0].split(u"><")
            # Az első a nyertes.
            nyertes_elemzes=guesser_elemzes[0]
        else:
            # Nincs guesser elemzés. -> Üres listát inicializálunk.
            guesser_elemzes=[]
            humor_elemzes=[elmezesek_raw2[0]]
            # A humor adta a nyertes elemzést.
            nyertes_elemzes=elmezesek_raw2[0]
        # Minden humor elemzés idegyűjtve.
        # Hozzáadjuk a többi elemzést a potenciális elsőhöz.
        humor_elemzes+=elmezesek_raw2[1:]
        # Sort, Uniq, formáz
        nyertes_tag=u"[" + u"[".join(nyertes_elemzes.split(u"[")[1:]) 
        nyertes_szoto=nyertes_elemzes.split(u"[")[0]
        if  not spellcheck and not szegedcheck:
            minden_elemzes_lista=map(lambda x :  re.sub(u'-$',"",x.split(u"[")[0]),filter(lambda x : felt(szo,x), list(set(guesser_elemzes + humor_elemzes))))
            for i in minden_elemzes_lista:
                lemmak[i]+=1
# újrefeldolgoz:

for l in lines:
    words=l.split()
    words_ki=[]
    for w in words:
        szo =            w.split(u"{{")[0]
        elemzesek_raw =  w.split(u"{{")[1].split(u"}}#")[0]
        spellcheck =bool(int(w.split(u"{{")[1].split(u"}}#")[1].split(u"#")[0]))
        szegedcheck=bool(int(w.split(u"{{")[1].split(u"}}#")[1].split(u"#")[1]))
        elmezesek_raw2=elemzesek_raw.split(u"||")
        if u"<" in elmezesek_raw2[0]:
            # Nem a 0. index az első humor elemzés -> Üres listát inicializálunk.
            humor_elemzes=[]
            # Guesser elemzések kigyűjtése.
            guesser_elemzes=elmezesek_raw2[0][1:].split(u">[")[0].split(u"><")
            # Az első a nyertes.
            nyertes_elemzes=guesser_elemzes[0]
        else:
            # Nincs guesser elemzés. -> Üres listát inicializálunk.
            guesser_elemzes=[]
            humor_elemzes=[elmezesek_raw2[0]]
            # A humor adta a nyertes elemzést.
            nyertes_elemzes=elmezesek_raw2[0]
        # Minden humor elemzés idegyűjtve.
        # Hozzáadjuk a többi elemzést a potenciális elsőhöz.
        humor_elemzes+=elmezesek_raw2[1:]
        # Sort, Uniq, formáz
        nyertes_tag=u"[" + u"[".join(nyertes_elemzes.split(u"[")[1:]) 
        nyertes_szoto=nyertes_elemzes.split(u"[")[0]
        if not spellcheck and not szegedcheck:
            minden_elemzes_lista=map(lambda x: (x,lemmak[x]) ,map(lambda x :  re.sub(u'-$',"",x.split(u"[")[0]),filter(lambda x : felt(szo,x), list(set(guesser_elemzes + humor_elemzes)))))
            if len(minden_elemzes_lista)>1:
                leggyakoribb = max(minden_elemzes_lista,key=lambda (x,y):y)
                lemmak2[leggyakoribb[0]]=leggyakoribb[1]
                elif len(minden_elemzes_lista)>0:
                    lemmak2[minden_elemzes_lista[0][0]]=minden_elemzes_lista[0][1]

for k,v in lemmak2.iteritems():
    if v>=3:
        #printout(unicode(v)+ u"#" + k)
        printout(k)
