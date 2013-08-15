"""

 ESTE CODIGO RELLENA LA BASE DE DATOS CON LOS ENLACES Y SUS RESPECTIVOS PESOS PARA
 LUEGO USARLOS CON NETSENSE PARA CONSTRUIR LOS GRAFOS (G).
 
 RECIBE 2 ARGUMENTOS: LA TABLA DE LA QUE SACA LOS ENTRENADOS Y UN BOOLEANO POR SI ESTA 
 EXTRACCION ES BALANCEADA (1) O DESBALANCEADA (0)

"""

from nltk.corpus import stopwords
import networkx as nx
import MySQLdb
import sys
import re

tabla=str(sys.argv[1])
balan=str(sys.argv[2])


leaves = "s"

if balan=="0":
	tabenlaces="enlaces_clasificador_0"
if balan=="1":
	tabenlaces="enlaces_clasificador_1"

# Open database connection
db = MySQLdb.connect("localhost","nodos","Tic2507*/","analitic")

# prepare a cursor object using cursor() method
c = db.cursor()

print "jajajajaj"

ides=0
c.execute("SELECT id_articulo FROM `clasificar_"+str(tabla)+"`")
resultado=c.fetchall()
for registro in resultado:
	ides=str(ides)+str(registro[0])+","
ides=str(ides[0:len(ides)-1])

print ides

##### HAGO EL BALANCE#####
balance=[]


c.execute("SELECT COUNT(*) FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=2 AND id_articulo NOT IN ("+ides+")") #NESTLE
#c.execute("SELECT COUNT(*) FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=2 AND `id_etiqueta`=1 AND id_articulo >2098") #BANCOS
#c.execute("SELECT COUNT(*) FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=2 AND `id_etiqueta`=80 AND id_articulo <128961") #CONCHA Y TORO
resultado=c.fetchall()
for neg in resultado:
	balance.append(neg[0])

c.execute("SELECT COUNT(*) FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=1 AND id_articulo NOT IN ("+ides+")") #NESTLE
#c.execute("SELECT COUNT(*) FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=0 AND `id_etiqueta`=1 AND id_articulo >2098") #BANCOS
#c.execute("SELECT COUNT(*) FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=0 AND `id_etiqueta`=80 AND id_articulo <128961") #CONCHA Y TORO
resultado=c.fetchall()
for neu in resultado:
	balance.append(neu[0])

c.execute("SELECT COUNT(*) FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=0 AND id_articulo NOT IN ("+ides+")") #NESTLE
#c.execute("SELECT COUNT(*) FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=1 AND `id_etiqueta`=1 AND id_articulo >2098") #BANCOS
#c.execute("SELECT COUNT(*) FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=1 AND `id_etiqueta`=80 AND id_articulo <128961") #CONCHA Y TORO
resultado=c.fetchall()
for pos in resultado:
	balance.append(pos[0])

bal=sorted(balance)

if balan=="1":
	min=bal[0]
if balan=="0":
	min=bal[2]

print min  # MIN ES EL LIMIT DE LA CONSULTA



##### TERMINO EL BALANCE#####



##### GENERO LA RED DE POSITIVOS #######
print "##### GENERO LA RED DE POSITIVOS #######"
c.execute("SELECT cuerpo FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=1 AND id_articulo NOT IN ("+ides+") LIMIT "+str(min)+" ")  
#c.execute("SELECT cuerpo FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=1 AND `id_etiqueta`=1 AND id_articulo >2098 LIMIT "+str(min)+" ") #BANCOS
#c.execute("SELECT cuerpo FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=1 AND `id_etiqueta`=80 AND id_articulo < 128961 LIMIT "+str(min)+" ") #CONCHA Y TORO
resultado=c.fetchall()

cuerpo=[]
cont=0
for reg in resultado:
    cuerpo.append(reg)
cuerpo=str(cuerpo)
#print cuerpo

""" EMOTICONES 
"""
cuerpo=cuerpo.replace(":)"," emoticonpositivo ")
cuerpo=cuerpo.replace("XD"," emoticonpositivo ")
cuerpo=cuerpo.replace("(:"," emoticonpositivo ")
cuerpo=cuerpo.replace(":D"," emoticonpositivo ")
cuerpo=cuerpo.replace(":-)"," emoticonpositivo ")
cuerpo=cuerpo.replace("(-:"," emoticonpositivo ")
cuerpo=cuerpo.replace("=D"," emoticonpositivo ")
cuerpo=cuerpo.replace("=)"," emoticonpositivo ")
cuerpo=cuerpo.replace("(="," emoticonpositivo ")
cuerpo=cuerpo.replace(";-)"," emoticonpositivo ")
cuerpo=cuerpo.replace(";)"," emoticonpositivo ")
cuerpo=cuerpo.replace(";D"," emoticonpositivo ")
cuerpo=cuerpo.replace("<3"," emoticonpositivo ")
    
cuerpo=cuerpo.replace(":("," emoticonegativo ")
cuerpo=cuerpo.replace("):"," emoticonegativo ")
cuerpo=cuerpo.replace(":-("," emoticonegativo ")
cuerpo=cuerpo.replace(")-:"," emoticonegativo ")
cuerpo=cuerpo.replace("D:"," emoticonegativo ")
cuerpo=cuerpo.replace("=D"," emoticonegativo ")
cuerpo=cuerpo.replace("=("," emoticonegativo ")
cuerpo=cuerpo.replace(")="," emoticonegativo ")
cuerpo=cuerpo.replace(":'("," emoticonegativo ")
cuerpo=cuerpo.replace("='["," emoticonegativo ")
cuerpo=cuerpo.replace(":_("," emoticonegativo ")
cuerpo=cuerpo.replace("/T_T"," emoticonegativo ")
cuerpo=cuerpo.replace("TOT"," emoticonegativo ")
cuerpo=cuerpo.replace(";_;"," emoticonegativo ")
    
    
cuerpo=cuerpo.lower()
    
""" reg exp letras repetidas 
"""
    
cuerpo=re.sub('a{2,}', 'a', cuerpo)
cuerpo=re.sub('b{2,}', 'b', cuerpo)
cuerpo=re.sub('c{2,}', 'c', cuerpo)
cuerpo=re.sub('d{2,}', 'd', cuerpo)
cuerpo=re.sub('e{2,}', 'e', cuerpo)
cuerpo=re.sub('f{2,}', 'f', cuerpo)
cuerpo=re.sub('g{2,}', 'g', cuerpo)
cuerpo=re.sub('h{2,}', 'h', cuerpo)
cuerpo=re.sub('i{2,}', 'i', cuerpo)
cuerpo=re.sub('j{2,}', 'j', cuerpo)
cuerpo=re.sub('k{2,}', 'k', cuerpo)
cuerpo=re.sub('m{2,}', 'm', cuerpo)
cuerpo=re.sub('n{2,}', 'n', cuerpo)
cuerpo=re.sub('o{2,}', 'o', cuerpo)
cuerpo=re.sub('p{2,}', 'p', cuerpo)
cuerpo=re.sub('q{2,}', 'q', cuerpo)
cuerpo=re.sub('s{2,}', 's', cuerpo)
cuerpo=re.sub('u{2,}', 'u', cuerpo)
cuerpo=re.sub('v{2,}', 'v', cuerpo)
cuerpo=re.sub('w{2,}', 'w', cuerpo)
cuerpo=re.sub('x{2,}', 'x', cuerpo)
cuerpo=re.sub('y{2,}', 'y', cuerpo)
cuerpo=re.sub('z{2,}', 'z', cuerpo)
    
""" borro caracteres raros 
"""


cuerpo=cuerpo.replace("/","")
cuerpo=cuerpo.replace("*","")
cuerpo=cuerpo.replace("\\","")
cuerpo=cuerpo.replace("\"","")
cuerpo=cuerpo.replace("%","")
cuerpo=cuerpo.replace(";","")
cuerpo=cuerpo.replace(",","")
cuerpo=cuerpo.replace(":","")
cuerpo=cuerpo.replace(".","")
cuerpo=cuerpo.replace("?","")
cuerpo=cuerpo.replace("!","")
cuerpo=cuerpo.replace("\'","")
cuerpo=cuerpo.replace("_","")
cuerpo=cuerpo.replace("-","")
cuerpo=cuerpo.replace("(","")
cuerpo=cuerpo.replace(")","")
cuerpo=cuerpo.replace("]","")
cuerpo=cuerpo.replace("[","")
cuerpo=cuerpo.replace("//","")
cuerpo=cuerpo.replace("<","")
cuerpo=cuerpo.replace(">","")

cuerpo=cuerpo.split()
    

#### TOKENIZACION

palabras=[]
for i in range (len(cuerpo)):
    #if cuerpo[i] not in stopwords.words('spanish') and len(cuerpo[i]) > 1:
    palabras.append(cuerpo[i])

#print palabras
#print "___________________"

##### NORMALIZACION

############# HASHTAGS, URLS Y DEMASES

for i in range (len(palabras)):
	if "@" in palabras[i]:
		palabras[i]="<MENCION>"
	if "#" in palabras[i]:
		palabras[i]="<HASHTAG>"
	if "www" in palabras[i] or "http" in palabras[i]:
		palabras[i]="<URL>"
	if "$" in palabras[i]:
		palabras[i]="<MONEDA>"
	if palabras[i].isdigit():
		palabras[i]="<NUMERO>"

############# PLURALES Y SUFIJOS
for leaf in leaves:
    for i in range (len(palabras)):
        if palabras[i][-len(leaf):] == leaf:
            palabras[i]=palabras[i][:-len(leaf)]


### BLOQUE PESOS ENLACES ###

pares=[]
for i in range (len(palabras)+1):
	if i<len(palabras)-1:
#		print str(palabras[i]) +" -> "+ str(palabras[i+1]) + "\n"
		pares.append(str(palabras[i])+" "+str(palabras[i+1]))

enlaces=[]
for w in pares:
	#print w
	
	for w2 in pares:
		if w == w2:
			cont=cont+1
			cont2=float(cont)
	#print str(w)+" "+str(cont)
	enlaces.append(str(w)+" "+str(1/cont2))
	cont=0

print "escribo enlaces positivos en la base de datos"
for ed in range (len(enlaces)):
	#enlaces=enlaces[ed]
	#print enlaces[ed].split(" ")
	links=enlaces[ed].split(" ")
	#print links[0],links[1],links[2]
	if links[0] not in stopwords.words('spanish') or links[1] not in stopwords.words('spanish') :
		#print "INSERT INTO `"+str(tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`tabla`,`stop_word`) VALUES ('"+str(links[0])+"','"+str(links[1])+"','"+str(links[2])+"','1','"+str(tabla)+"','0')"
		c.execute("INSERT INTO `"+str(tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`tabla`,`stop_word`) VALUES ('"+str(links[0])+"','"+str(links[1])+"','"+str(links[2])+"','1','"+str(tabla)+"','0')")
	else:
		c.execute("INSERT INTO `"+str(tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`tabla`,`stop_word`) VALUES ('"+str(links[0])+"','"+str(links[1])+"','"+str(links[2])+"','1','"+str(tabla)+"','1')")
### FIN BLOQUE PESOS ENLACES ###




print "##### GENERO LA RED DE NEGATIVOS #######"
##### GENERO LA RED DE NEGATIVOS #######
c.execute("SELECT cuerpo FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=2 AND id_articulo NOT IN ("+ides+") LIMIT "+str(min)+" ") #MOVISTAR
#c.execute("SELECT cuerpo FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=2 AND `id_etiqueta`=1 AND id_articulo >2098 LIMIT "+str(min)+" ") #BANCOS
#c.execute("SELECT cuerpo FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=2 AND `id_etiqueta`=80 AND id_articulo < 128961 LIMIT "+str(min)+" ") #CONCHA Y TORO
resultado=c.fetchall()

cuerpo2=[]
cont2=0
for reg in resultado:
    cuerpo2.append(reg)

cuerpo2=str(cuerpo2)

""" EMOTICONES 
"""
cuerpo2=cuerpo2.replace(":)"," emoticonpositivo ")
cuerpo2=cuerpo2.replace("XD"," emoticonpositivo ")
cuerpo2=cuerpo2.replace("(:"," emoticonpositivo ")
cuerpo2=cuerpo2.replace(":D"," emoticonpositivo ")
cuerpo2=cuerpo2.replace(":-)"," emoticonpositivo ")
cuerpo2=cuerpo2.replace("(-:"," emoticonpositivo ")
cuerpo2=cuerpo2.replace("=D"," emoticonpositivo ")
cuerpo2=cuerpo2.replace("=)"," emoticonpositivo ")
cuerpo2=cuerpo2.replace("(="," emoticonpositivo ")
cuerpo2=cuerpo2.replace(";-)"," emoticonpositivo ")
cuerpo2=cuerpo2.replace(";)"," emoticonpositivo ")
cuerpo2=cuerpo2.replace(";D"," emoticonpositivo ")
cuerpo2=cuerpo2.replace("<3"," emoticonpositivo ")
    
cuerpo2=cuerpo2.replace(":("," emoticonegativo ")
cuerpo2=cuerpo2.replace("):"," emoticonegativo ")
cuerpo2=cuerpo2.replace(":-("," emoticonegativo ")
cuerpo2=cuerpo2.replace(")-:"," emoticonegativo ")
cuerpo2=cuerpo2.replace("D:"," emoticonegativo ")
cuerpo2=cuerpo2.replace("=D"," emoticonegativo ")
cuerpo2=cuerpo2.replace("=("," emoticonegativo ")
cuerpo2=cuerpo2.replace(")="," emoticonegativo ")
cuerpo2=cuerpo2.replace(":'("," emoticonegativo ")
cuerpo2=cuerpo2.replace("='["," emoticonegativo ")
cuerpo2=cuerpo2.replace(":_("," emoticonegativo ")
cuerpo2=cuerpo2.replace("/T_T"," emoticonegativo ")
cuerpo2=cuerpo2.replace("TOT"," emoticonegativo ")
cuerpo2=cuerpo2.replace(";_;"," emoticonegativo ")
    
    
cuerpo2=cuerpo2.lower()
    
""" reg exp letras repetidas 
"""
    
cuerpo2=re.sub('a{2,}', 'a', cuerpo2)
cuerpo2=re.sub('b{2,}', 'b', cuerpo2)
cuerpo2=re.sub('c{2,}', 'c', cuerpo2)
cuerpo2=re.sub('d{2,}', 'd', cuerpo2)
cuerpo2=re.sub('e{2,}', 'e', cuerpo2)
cuerpo2=re.sub('f{2,}', 'f', cuerpo2)
cuerpo2=re.sub('g{2,}', 'g', cuerpo2)
cuerpo2=re.sub('h{2,}', 'h', cuerpo2)
cuerpo2=re.sub('i{2,}', 'i', cuerpo2)
cuerpo2=re.sub('j{2,}', 'j', cuerpo2)
cuerpo2=re.sub('k{2,}', 'k', cuerpo2)
cuerpo2=re.sub('m{2,}', 'm', cuerpo2)
cuerpo2=re.sub('n{2,}', 'n', cuerpo2)
cuerpo2=re.sub('o{2,}', 'o', cuerpo2)
cuerpo2=re.sub('p{2,}', 'p', cuerpo2)
cuerpo2=re.sub('q{2,}', 'q', cuerpo2)
cuerpo2=re.sub('s{2,}', 's', cuerpo2)
cuerpo2=re.sub('u{2,}', 'u', cuerpo2)
cuerpo2=re.sub('v{2,}', 'v', cuerpo2)
cuerpo2=re.sub('w{2,}', 'w', cuerpo2)
cuerpo2=re.sub('x{2,}', 'x', cuerpo2)
cuerpo2=re.sub('y{2,}', 'y', cuerpo2)
cuerpo2=re.sub('z{2,}', 'z', cuerpo2)
    
""" borro caracteres raros 
"""


cuerpo2=cuerpo2.replace("/","")
cuerpo2=cuerpo2.replace("*","")
cuerpo2=cuerpo2.replace("\\","")
cuerpo2=cuerpo2.replace("\"","")
cuerpo2=cuerpo2.replace("%","")
cuerpo2=cuerpo2.replace(";","")
cuerpo2=cuerpo2.replace(",","")
cuerpo2=cuerpo2.replace(":","")
cuerpo2=cuerpo2.replace(".","")
cuerpo2=cuerpo2.replace("?","")
cuerpo2=cuerpo2.replace("!","")
cuerpo2=cuerpo2.replace("\'","")
cuerpo2=cuerpo2.replace("_","")
cuerpo2=cuerpo2.replace("-","")
cuerpo2=cuerpo2.replace("(","")
cuerpo2=cuerpo2.replace(")","")
cuerpo2=cuerpo2.replace("]","")
cuerpo2=cuerpo2.replace("[","")
cuerpo2=cuerpo2.replace("//","")
cuerpo2=cuerpo2.replace("<","")
cuerpo2=cuerpo2.replace(">","")

cuerpo2=cuerpo2.split()
    

#### TOKENIZACION

palabras2=[]
for i in range (len(cuerpo2)):
    #if cuerpo2[i] not in stopwords.words('spanish') and len(cuerpo2[i]) > 1:
    palabras2.append(cuerpo2[i])

#print palabras2
#print "___________________"

##### NORMALIZACION

############# HASHTAGS, URLS Y DEMASES

for i in range (len(palabras2)):
	if "@" in palabras2[i]:
		palabras2[i]="<MENCION>"
	if "#" in palabras2[i]:
		palabras2[i]="<HASHTAG>"
	if "www" in palabras2[i] or "http" in palabras2[i]:
		palabras2[i]="<URL>"
	if "$" in palabras2[i]:
		palabras2[i]="<MONEDA>"
	if palabras2[i].isdigit():
		palabras2[i]="<NUMERO>"

############# PLURALES Y SUFIJOS
for leaf in leaves:
    for i in range (len(palabras2)):
        if palabras2[i][-len(leaf):] == leaf:
            palabras2[i]=palabras2[i][:-len(leaf)]


### BLOQUE PESOS ENLACES ###

pares2=[]
for i in range (len(palabras2)+1):
	if i<len(palabras2)-1:
		#print str(palabras2[i]) +" -> "+ str(palabras2[i+1]) + "\n"
		pares2.append(str(palabras2[i])+" "+str(palabras2[i+1]))

enlaces2=[]
for w2 in pares2:
	#print w
	
	for w22 in pares2:
		if w2 == w22:
			cont2=cont2+1
			cont22=float(cont2)
	#print str(w2)+" "+str(cont2)
	enlaces2.append(str(w2)+" "+str(1/cont22))
	cont2=0

print "escribo enlaces negativos en la base de datos"
for ed2 in range (len(enlaces2)):
	#enlaces2=enlaces2[ed2]
	#print enlaces2[ed2].split(" ")
	links2=enlaces2[ed2].split(" ")
	if links2[0] not in stopwords.words('spanish') or links2[1] not in stopwords.words('spanish') :
		c.execute("INSERT INTO `"+str(tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`tabla`,`stop_word`) VALUES ('"+str(links2[0])+"','"+str(links2[1])+"','"+str(links2[2])+"','2','"+str(tabla)+"','0')")
	else:
		c.execute("INSERT INTO `"+str(tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`tabla`,`stop_word`) VALUES ('"+str(links2[0])+"','"+str(links2[1])+"','"+str(links2[2])+"','2','"+str(tabla)+"','1')")
### FIN BLOQUE PESOS ENLACES ###



##### GENERO LA RED DE NEUTROS #######
print "##### GENERO LA RED DE NEUTROS #######"
c.execute("SELECT cuerpo FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=0 AND id_articulo NOT IN ("+ides+") LIMIT "+str(min)+" ") #MOVISTAR
#c.execute("SELECT cuerpo FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=0 AND `id_etiqueta`=1 AND id_articulo >2098 LIMIT "+str(min)+" ") #BANCOS
#c.execute("SELECT cuerpo FROM `"+str(tabla)+"` WHERE `plataforma`=0 AND `clasificado`=1 AND `sentido_manual`=0 AND `id_etiqueta`=80 AND id_articulo < 128961 LIMIT "+str(min)+" ") #CONCHA Y TORO
resultado=c.fetchall()


cuerpo3=[]
cont3=0
for reg in resultado:
    cuerpo3.append(reg)

cuerpo3=str(cuerpo3)

""" EMOTICONES 
"""
cuerpo3=cuerpo3.replace(":)"," emoticonpositivo ")
cuerpo3=cuerpo3.replace("XD"," emoticonpositivo ")
cuerpo3=cuerpo3.replace("(:"," emoticonpositivo ")
cuerpo3=cuerpo3.replace(":D"," emoticonpositivo ")
cuerpo3=cuerpo3.replace(":-)"," emoticonpositivo ")
cuerpo3=cuerpo3.replace("(-:"," emoticonpositivo ")
cuerpo3=cuerpo3.replace("=D"," emoticonpositivo ")
cuerpo3=cuerpo3.replace("=)"," emoticonpositivo ")
cuerpo3=cuerpo3.replace("(="," emoticonpositivo ")
cuerpo3=cuerpo3.replace(";-)"," emoticonpositivo ")
cuerpo3=cuerpo3.replace(";)"," emoticonpositivo ")
cuerpo3=cuerpo3.replace(";D"," emoticonpositivo ")
cuerpo3=cuerpo3.replace("<3"," emoticonpositivo ")
    
cuerpo3=cuerpo3.replace(":("," emoticonegativo ")
cuerpo3=cuerpo3.replace("):"," emoticonegativo ")
cuerpo3=cuerpo3.replace(":-("," emoticonegativo ")
cuerpo3=cuerpo3.replace(")-:"," emoticonegativo ")
cuerpo3=cuerpo3.replace("D:"," emoticonegativo ")
cuerpo3=cuerpo3.replace("=D"," emoticonegativo ")
cuerpo3=cuerpo3.replace("=("," emoticonegativo ")
cuerpo3=cuerpo3.replace(")="," emoticonegativo ")
cuerpo3=cuerpo3.replace(":'("," emoticonegativo ")
cuerpo3=cuerpo3.replace("='["," emoticonegativo ")
cuerpo3=cuerpo3.replace(":_("," emoticonegativo ")
cuerpo3=cuerpo3.replace("/T_T"," emoticonegativo ")
cuerpo3=cuerpo3.replace("TOT"," emoticonegativo ")
cuerpo3=cuerpo3.replace(";_;"," emoticonegativo ")
    
    
cuerpo3=cuerpo3.lower()
    
""" reg exp letras repetidas 
"""
    
cuerpo3=re.sub('a{2,}', 'a', cuerpo3)
cuerpo3=re.sub('b{2,}', 'b', cuerpo3)
cuerpo3=re.sub('c{2,}', 'c', cuerpo3)
cuerpo3=re.sub('d{2,}', 'd', cuerpo3)
cuerpo3=re.sub('e{2,}', 'e', cuerpo3)
cuerpo3=re.sub('f{2,}', 'f', cuerpo3)
cuerpo3=re.sub('g{2,}', 'g', cuerpo3)
cuerpo3=re.sub('h{2,}', 'h', cuerpo3)
cuerpo3=re.sub('i{2,}', 'i', cuerpo3)
cuerpo3=re.sub('j{2,}', 'j', cuerpo3)
cuerpo3=re.sub('k{2,}', 'k', cuerpo3)
cuerpo3=re.sub('m{2,}', 'm', cuerpo3)
cuerpo3=re.sub('n{2,}', 'n', cuerpo3)
cuerpo3=re.sub('o{2,}', 'o', cuerpo3)
cuerpo3=re.sub('p{2,}', 'p', cuerpo3)
cuerpo3=re.sub('q{2,}', 'q', cuerpo3)
cuerpo3=re.sub('s{2,}', 's', cuerpo3)
cuerpo3=re.sub('u{2,}', 'u', cuerpo3)
cuerpo3=re.sub('v{2,}', 'v', cuerpo3)
cuerpo3=re.sub('w{2,}', 'w', cuerpo3)
cuerpo3=re.sub('x{2,}', 'x', cuerpo3)
cuerpo3=re.sub('y{2,}', 'y', cuerpo3)
cuerpo3=re.sub('z{2,}', 'z', cuerpo3)
    
""" borro caracteres raros 
"""


cuerpo3=cuerpo3.replace("/","")
cuerpo3=cuerpo3.replace("*","")
cuerpo3=cuerpo3.replace("\\","")
cuerpo3=cuerpo3.replace("\"","")
cuerpo3=cuerpo3.replace("%","")
cuerpo3=cuerpo3.replace(";","")
cuerpo3=cuerpo3.replace(",","")
cuerpo3=cuerpo3.replace(":","")
cuerpo3=cuerpo3.replace(".","")
cuerpo3=cuerpo3.replace("?","")
cuerpo3=cuerpo3.replace("!","")
cuerpo3=cuerpo3.replace("\'","")
cuerpo3=cuerpo3.replace("_","")
cuerpo3=cuerpo3.replace("-","")
cuerpo3=cuerpo3.replace("(","")
cuerpo3=cuerpo3.replace(")","")
cuerpo3=cuerpo3.replace("]","")
cuerpo3=cuerpo3.replace("[","")
cuerpo3=cuerpo3.replace("//","")
cuerpo3=cuerpo3.replace("<","")
cuerpo3=cuerpo3.replace(">","")

cuerpo3=cuerpo3.split()
    

#### TOKENIZACION

palabras3=[]
for i in range (len(cuerpo3)):
    #if cuerpo3[i] not in stopwords.words('spanish') and len(cuerpo3[i]) > 1:
    palabras3.append(cuerpo3[i])

#print palabras3
#print "___________________"

##### NORMALIZACION

############# HASHTAGS, URLS Y DEMASES

for i in range (len(palabras3)):
	if "@" in palabras3[i]:
		palabras3[i]="<MENCION>"
	if "#" in palabras3[i]:
		palabras3[i]="<HASHTAG>"
	if "www" in palabras3[i] or "http" in palabras3[i]:
		palabras3[i]="<URL>"
	if "$" in palabras3[i]:
		palabras3[i]="<MONEDA>"
	if palabras3[i].isdigit():
		palabras3[i]="<NUMERO>"

############# PLURALES Y SUFIJOS
for leaf in leaves:
    for i in range (len(palabras3)):
        if palabras3[i][-len(leaf):] == leaf:
            palabras3[i]=palabras3[i][:-len(leaf)]


### BLOQUE PESOS ENLACES ###

pares3=[]
for i in range (len(palabras3)+1):
	if i<len(palabras3)-1:
		#print str(palabras3[i]) +" -> "+ str(palabras3[i+1]) + "\n"
		pares3.append(str(palabras3[i])+" "+str(palabras3[i+1]))

enlaces3=[]
for w3 in pares3:
	#print w
	
	for w32 in pares3:
		if w3 == w32:
			cont3=cont3+1
			cont32=float(cont3)
	#print str(w3)+" "+str(cont3)
	enlaces3.append(str(w3)+" "+str(1/cont32))
	cont3=0

print "escribo enlaces neutros"
for ed3 in range (len(enlaces3)):
	#enlaces3=enlaces3[ed3]
	#print enlaces3[ed3].split(" ")
	links3=enlaces3[ed3].split(" ")
	if links3[0] not in stopwords.words('spanish') or links3[1] not in stopwords.words('spanish') :
		c.execute("INSERT INTO `"+str(tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`tabla`,`stop_word`) VALUES ('"+str(links3[0])+"','"+str(links3[1])+"','"+str(links3[2])+"','0','"+str(tabla)+"','0')")
	else:
		c.execute("INSERT INTO `"+str(tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`tabla`,`stop_word`) VALUES ('"+str(links3[0])+"','"+str(links3[1])+"','"+str(links3[2])+"','0','"+str(tabla)+"','1')")

### FIN BLOQUE PESOS ENLACES ###


db.close()
