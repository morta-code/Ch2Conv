# Ch2Conv
Környezetfüggetlen nyelvtannal leírható nyelvek közti konverziót megvalósító alkalmazás

### Használat
+ ch2conv definitions.yml
Olvasás és írás a std. in és outputtal

+ ch2conv definitions.yml -i input -o output
Olvasás és írás a megadott fájlokból (vegyíthető az előzővel).

### Definíciók
Szabványos YAML fájl, kötelező megadni, és két fő része van:
+ lexers
+ syntax

A lexers résszel definiálunk tokenizálókat (tömbbe rendezve), mégpedig úgy, hogy tömbbe rendezve felsoroljuk a szabályokat.

A szabályok a következő alakúak lehetnek az első lexernél:

	név: [regexp, opt]

ahol a regexp érvényes reguláris kifejezés és perl-tipusú előretekintés lehet, az opt pedig yes, ha tovább kell vinni a lexémát, no, ha nem, vagy egy függvénynév ha külső feldolgozást is szeretnénk a lexémán. Nem kötelező megadni, default érték a yes (ekkor tömb sem kell).

Kucsszavak a szabályokban:

	__maxlength__: hossz
	__ignore__: regexp

Megadható a szövegforrásnál a maximális lexéma hossz (nem kötelező, de biztonságot ad), illetve megadható, milyen lexémákból ne generáljon tokent (több is megadható), pl. kommentek esetén.

A második lexertől a szabály örökölhető tokenneveket tartalmaz. Ha nincs értéke, feldolgozás nélkül tovább adja, ha pedig feldolgozás szükséges, tömbben felsorolva adjuk meg a fentihez hasonló szabályokat. Fontos, hogy nem lehe ismétlődés a tokennevekben, mert az elemzés közben félreértéshez vzetne.

TODO: a regexp mindenhol helyettesíthető kételemű tömbbel, ahol a lexéma eleje és a vége adható meg, hosszabb lexémák esetén. Még nincs implementálva

#### Példa

	lexers:
	    - első:
	        - __maxlength__: 40 
	        - __ignore__: '#(?![01]).+'
	        - space: [' ', no]
	        - newparagraph: ['\n\n', no]
	        - newsentence: ['\n', no]
	        - word: ['[^\s]+', yes]
	    - második:
	        - newparagraph
	        - newsentence
	        - word:
	            - tag: ['\[\w+\]', yes]
	            - multitag: ['\[\w+\|\w+\]', yes]
	            - delim: ['\|\|', no]
	            - opentags: ['\{\{', no]
	            - closetags: ['\}\}', no]
	            - bool: ['#[01]', yes] #tipikus példa az utófeldolgozásra, # levétele
	            - opendict: ['<', no]
	            - closedict: ['>', no]
	            - w: ['[^|{}<>#\[\]\n]+', yes]
