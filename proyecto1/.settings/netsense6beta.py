"""
ESTA NUEVA VERSION CONSIDERA LA NORMALIZACION DE LOS MENSAJES

CLASIFICADOR QUE LEE TWEETS A CLASIFICAR DESDE LA TABLA CLASIFICAR+TABLA 
Y DESDE ENLACES_CLASIFICADOR SACA LAS REDES G

RECIBE 4 ARGUMENTOS:

-TABLA,
-TIPO DE ANALISIS (NO-WEIGHT,WEIGHT),
-STOP-WORDS (SI=1, NO=0),
-BALANCE (SI=1, NO=0)
 

"""


from nltk.corpus import stopwords
import networkx as nx
import MySQLdb
import sys
import re


tabla=str(sys.argv[1])
w=str(sys.argv[2])
stpw=str(sys.argv[3])
balance=str(sys.argv[4])
ponderapares=sys.argv[5]
ponderadis=sys.argv[6]
umbralpeso=sys.argv[7]

#f=open("resultados_"+str(tabla)+"_"+str(w)+"_"+str(stpw)+"_"+str(balance)+"_"+str(ponderapares)+".txt","w")

print 'tabla: '+str(tabla)
print 'tipo de analisis: '+str(w)
print 'stopwords: '+str(stpw)
print 'balance: '+str(balance)
print 'ponderapares: '+str(ponderapares)
print 'ponderadis: '+str(ponderadis)
print 'umbral peso: '+str(umbralpeso)
print '_*_*_*_*_*_*_*_*_*_*\n'

#f.write('tabla: '+str(tabla))
#f.write('\ntipo de analisis: '+str(w))
#f.write( '\nstopwords: '+str(stpw))
#f.write( '\nbalance: '+str(balance))
#f.write( '\nponderapares: '+str(ponderapares))
#f.write( '\nponderadis: '+str(ponderadis))
#f.write( '\numbralpeso: '+str(umbralpeso))

if w=="netsense_w":
		analisis=1
if w=="netsense":
		analisis=0
	

leaves = "s"


# Open database connection
db = MySQLdb.connect("localhost","root","","analitic")

# prepare a cursor object using cursor() method
c = db.cursor()


#print "##### GENERO LA RED DE POSITIVOS #######"

g = nx.DiGraph()

if stpw=="0":
	if balance=="0":
		#print "Estoy haciendo la red de positivos desde la tabla "+str(tabla)+" sin stopwords y entrenados desbalanceados."
		c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_0` WHERE `sentido_manual`=1 AND `tabla`='"+str(tabla)+"' AND `stop_word`='0' AND `weight`<="+str(umbralpeso)+" ")
		#c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_0` WHERE `sentido_manual`=1 AND `stop_word`='0' ") # TOMA TODOS LOS ENLACES DE TODAS LAS TABLAS
		resultadoC1=c.fetchall()
	if balance=="1":
		#print "Estoy haciendo la red de positivos desde la tabla "+str(tabla)+" sin stopwords y entrenados balanceados."
		c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_1` WHERE `sentido_manual`=1 AND `tabla`='"+str(tabla)+"' AND `stop_word`='0' AND `weight`<="+str(umbralpeso)+" ")
		#c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_1` WHERE `sentido_manual`=1 AND `stop_word`='0' ") # TOMA TODOS LOS ENLACES DE TODAS LAS TABLAS
		resultadoC1=c.fetchall()
	
if stpw=="1":
	if balance=="0":
		#print "Estoy haciendo la red de positivos desde la tabla "+str(tabla)+" con stopwords y entrenados desbalanceados."
		c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_0` WHERE `sentido_manual`=1 AND `tabla`='"+str(tabla)+"'  AND `weight`<="+str(umbralpeso)+" ")
		#c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_0` WHERE `sentido_manual`=1 ") # TOMA TODOS LOS ENLACES DE TODAS LAS TABLAS
		resultadoC1=c.fetchall()
	if balance=="1":
		#print "Estoy haciendo la red de positivos desde la tabla "+str(tabla)+" con stopwords y entrenados balanceados."
		c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_1` WHERE `sentido_manual`=1 AND `tabla`='"+str(tabla)+"'  AND `weight`<="+str(umbralpeso)+" ")
		#c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_1` WHERE `sentido_manual`=1 ") # TOMA TODOS LOS ENLACES DE TODAS LAS TABLAS
		resultadoC1=c.fetchall()

for reg1 in resultadoC1:
	g.add_edge(reg1[0],reg1[1],weight=float(reg1[2]))



#print "##### GENERO LA RED DE NEGATIVOS #######"

h = nx.DiGraph()

if stpw=="0":
	if balance=="0":
		#print "Estoy haciendo la red de negativos desde la tabla "+str(tabla)+" sin stopwords y entrenados desbalanceados."
		c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_0` WHERE `sentido_manual`=2 AND `tabla`='"+str(tabla)+"' AND `stop_word`='0'  AND `weight`<="+str(umbralpeso)+" ")
		#c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_0` WHERE `sentido_manual`=2 AND `stop_word`='0' ") # TOMA TODOS LOS ENLACES DE TODAS LAS TABLAS
		resultadoC2=c.fetchall()
	if balance=="1":
		#print "Estoy haciendo la red de negativos desde la tabla "+str(tabla)+" sin stopwords y entrenados balanceados."
		c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_1` WHERE `sentido_manual`=2 AND `tabla`='"+str(tabla)+"' AND `stop_word`='0'  AND `weight`<="+str(umbralpeso)+" ")
		#c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_1` WHERE `sentido_manual`=2 AND `stop_word`='0' ") # TOMA TODOS LOS ENLACES DE TODAS LAS TABLAS
		resultadoC2=c.fetchall()
	
if stpw=="1":
	if balance=="0":
		#print "Estoy haciendo la red de negativos desde la tabla "+str(tabla)+" con stopwords y entrenados desbalanceados."
		c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_0` WHERE `sentido_manual`=2 AND `tabla`='"+str(tabla)+"'  AND `weight`<="+str(umbralpeso)+" ")
		#c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_0` WHERE `sentido_manual`=2 ") # TOMA TODOS LOS ENLACES DE TODAS LAS TABLAS
		resultadoC2=c.fetchall()
	if balance=="1":
		#print "Estoy haciendo la red de negativos desde la tabla "+str(tabla)+" con stopwords y entrenados balanceados."
		c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_1` WHERE `sentido_manual`=2 AND `tabla`='"+str(tabla)+"'  AND `weight`<="+str(umbralpeso)+" ")
		#c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_1` WHERE `sentido_manual`=2 ") # TOMA TODOS LOS ENLACES DE TODAS LAS TABLAS
		resultadoC2=c.fetchall()
	
for reg2 in resultadoC2:
	h.add_edge(reg2[0],reg2[1],weight=float(reg2[2]))
	


#print "##### GENERO LA RED DE NEUTROS #######"

nt = nx.DiGraph()

if stpw=="0":
	if balance=="0":
		#print "Estoy haciendo la red de neutros desde la tabla "+str(tabla)+" sin stopwords y entrenados desbalanceados."
		c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_0` WHERE `sentido_manual`=0 AND `tabla`='"+str(tabla)+"' AND `stop_word`='0'  AND `weight`<="+str(umbralpeso)+" ")
		#c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_0` WHERE `sentido_manual`=0 AND `stop_word`='0' ") # TOMA TODOS LOS ENLACES DE TODAS LAS TABLAS
		resultadoC3=c.fetchall()
	if balance=="1":
		#print "Estoy haciendo la red de neutros desde la tabla "+str(tabla)+" sin stopwords y entrenados balanceados."
		c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_1` WHERE `sentido_manual`=0 AND `tabla`='"+str(tabla)+"' AND `stop_word`='0'  AND `weight`<="+str(umbralpeso)+" ")
		#c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_1` WHERE `sentido_manual`=0 AND `stop_word`='0' ") # TOMA TODOS LOS ENLACES DE TODAS LAS TABLAS
		resultadoC3=c.fetchall()
	
if stpw=="1":
	if balance=="0":
		#print "Estoy haciendo la red de neutros desde la tabla "+str(tabla)+" con stopwords y entrenados desbalanceados."
		c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_0` WHERE `sentido_manual`=0 AND `tabla`='"+str(tabla)+"'  AND `weight`<="+str(umbralpeso)+" ")
		#c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_0` WHERE `sentido_manual`=0 ") # TOMA TODOS LOS ENLACES DE TODAS LAS TABLAS
		resultadoC3=c.fetchall()
	if balance=="1":
		#print "Estoy haciendo la red de neutros desde la tabla "+str(tabla)+" con stopwords y entrenados balanceados."
		c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_1` WHERE `sentido_manual`=0 AND `tabla`='"+str(tabla)+"'  AND `weight`<="+str(umbralpeso)+" ")
		#c.execute(" SELECT `palabra_source`,`palabra_target`,`weight` FROM `enlaces_clasificador_1` WHERE `sentido_manual`=0 ") # TOMA TODOS LOS ENLACES DE TODAS LAS TABLAS
		resultadoC3=c.fetchall()	

for reg3 in resultadoC3:
	nt.add_edge(reg3[0],reg3[1],weight=float(reg3[2]))
	
enlaces=g.edges()
enlaces2=h.edges()
enlaces3=nt.edges()

nodos=[]	
nodes = g.nodes()
nodos.append(len(nodes))
nodes2 = h.nodes()
nodos.append(len(nodes2))
nodes3 = nt.nodes()
nodos.append(len(nodes3))

bal=sorted(nodos)

#float(ponderapares)

balpos=1-(float(len(nodes)))/bal[2]
balneg=1-(float(len(nodes2)))/bal[2]
balneu=1-(float(len(nodes3)))/bal[2]




#print "Datos de la red"
#print "Nodos +: "+str(len(n odes))+" Enlaces +: "+str(len(enlaces))
nodpos=float(len(nodes))
#print "Nodos -: "+str(len(nodes2))+" Enlaces +: "+str(len(enlaces2))
nodneg=float(len(nodes2))
#print "Nodos o: "+str(len(nodes3))+" Enlaces +: "+str(len(enlaces3))
nodneu=float(len(nodes3))




##### ESCOJO TWEETS A EVALUAR #######
#c.execute("SELECT cuerpo,id_articulo,sentido FROM `movistar` WHERE `clasificado`=1 AND plataforma=0 AND `id_articulo` >= 502758")
c.execute(" SELECT cuerpo,id_articulo FROM `clasificar_"+str(tabla)+"` ") # WHERE id_articulo=214
resultadotweet=c.fetchall()



for regtweetx in resultadotweet:
	twe=regtweetx[0].replace("'","")
	#print "INSERT INTO `clasificar_movistar`(`id_articulo`,`cuerpo`,`sentido_manual`) VALUES ('"+str(regtweetx[1])+"','"+str(twe)+"','"+str(regtweetx[2])+"')"
	#c.execute("INSERT INTO `clasificar_"+str(tabla)+"` (`id_articulo`,`cuerpo`,`sentido_manual`) VALUES ('"+str(regtweetx[1])+"','"+str(twe)+"','"+str(regtweetx[2])+"')")

id=[]
tweet=[]
contweet=0
for regtweet in resultadotweet:
    contweet=contweet+1
    tweet=regtweet[0]
    id=str(regtweet[1])
    #print "__________________________________"
    #print "id: " +str(id)
    #print "_____________________________________________"
    
    
    
    #tweet="caca"

    tweet=str(tweet)
    
    #print str(contweet)+") " + str(tweet) + "-> id:" +str(id)
    
    
    """ EMOTICONES 
    """
    tweet=tweet.replace(":)"," emoticonpositivo ")
    tweet=tweet.replace("XD"," emoticonpositivo ")
    tweet=tweet.replace("(:"," emoticonpositivo ")
    tweet=tweet.replace(":D"," emoticonpositivo ")
    tweet=tweet.replace(":-)"," emoticonpositivo ")
    tweet=tweet.replace("(-:"," emoticonpositivo ")
    tweet=tweet.replace("=D"," emoticonpositivo ")
    tweet=tweet.replace("=)"," emoticonpositivo ")
    tweet=tweet.replace("(="," emoticonpositivo ")
    tweet=tweet.replace(";-)"," emoticonpositivo ")
    tweet=tweet.replace(";)"," emoticonpositivo ")
    tweet=tweet.replace(";D"," emoticonpositivo ")
    tweet=tweet.replace("<3"," emoticonpositivo ")
    
    tweet=tweet.replace(":("," emoticonegativo ")
    tweet=tweet.replace("):"," emoticonegativo ")
    tweet=tweet.replace(":-("," emoticonegativo ")
    tweet=tweet.replace(")-:"," emoticonegativo ")
    tweet=tweet.replace("D:"," emoticonegativo ")
    tweet=tweet.replace("=D"," emoticonegativo ")
    tweet=tweet.replace("=("," emoticonegativo ")
    tweet=tweet.replace(")="," emoticonegativo ")
    tweet=tweet.replace(":'("," emoticonegativo ")
    tweet=tweet.replace("='["," emoticonegativo ")
    tweet=tweet.replace(":_("," emoticonegativo ")
    tweet=tweet.replace("/T_T"," emoticonegativo ")
    tweet=tweet.replace("TOT"," emoticonegativo ")
    tweet=tweet.replace(";_;"," emoticonegativo ")
    
    tweet=tweet.replace("RT"," ")
    
    tweet=tweet.lower()
    
    """ reg exp letras repetidas 
    """
    
    tweet=re.sub('a{2,}', 'a', tweet)
    tweet=re.sub('b{2,}', 'b', tweet)
    tweet=re.sub('c{2,}', 'c', tweet)
    tweet=re.sub('d{2,}', 'd', tweet)
    tweet=re.sub('e{2,}', 'e', tweet)
    tweet=re.sub('f{2,}', 'f', tweet)
    tweet=re.sub('g{2,}', 'g', tweet)
    tweet=re.sub('h{2,}', 'h', tweet)
    tweet=re.sub('i{2,}', 'i', tweet)
    tweet=re.sub('j{2,}', 'j', tweet)
    tweet=re.sub('k{2,}', 'k', tweet)
    tweet=re.sub('m{2,}', 'm', tweet)
    tweet=re.sub('n{2,}', 'n', tweet)
    tweet=re.sub('o{2,}', 'o', tweet)
    tweet=re.sub('p{2,}', 'p', tweet)
    tweet=re.sub('q{2,}', 'q', tweet)
    tweet=re.sub('s{2,}', 's', tweet)
    tweet=re.sub('u{2,}', 'u', tweet)
    tweet=re.sub('v{2,}', 'v', tweet)
    tweet=re.sub('w{2,}', 'w', tweet)
    tweet=re.sub('x{2,}', 'x', tweet)
    tweet=re.sub('y{2,}', 'y', tweet)
    tweet=re.sub('z{2,}', 'z', tweet)
    
    """ borro caracteres raros 
    """
    tweet=tweet.replace("/","")
    tweet=tweet.replace("*","")
    tweet=tweet.replace("\\","")
    tweet=tweet.replace("\"","")
    tweet=tweet.replace("%","")
    tweet=tweet.replace(";","")
    tweet=tweet.replace(",","")
    tweet=tweet.replace(":","")
    tweet=tweet.replace(".","")
    tweet=tweet.replace("?","")
    tweet=tweet.replace("!","")
    tweet=tweet.replace("\'","")
    tweet=tweet.replace("_","")
    tweet=tweet.replace("-","")
    tweet=tweet.replace("(","")
    tweet=tweet.replace(")","")
    tweet=tweet.replace("]","")
    tweet=tweet.replace("[","")
    tweet=tweet.replace("//","")
    tweet=tweet.replace("<","")
    tweet=tweet.replace(">","")
    
    #print tweet
    
    tweet=tweet.split()

    tweetwords=[]
    anew=0
    val=0
    valence=0
    emoticonpos=0
    emoticonneg=0
    for i in range (len(tweet)):
        #print tweet[i]
        if tweet[i]=="emoticonpositivo":
            emoticonpos=emoticonpos+1
            #print ":)" 
        if tweet[i]=="emoticonegativo":
            emoticonneg=emoticonneg+1
            #print ":("
        
        if stpw=="0":
            if tweet[i] not in stopwords.words('spanish') and len(tweet[i]) > 1:
                tweetwords.append(tweet[i])
                    
        if stpw=="1":
            tweetwords.append(tweet[i])
        

###  AQUI VEO SI LAS PALABRAS TIENEN VALOR EN ANEW ###        
    contval=1
    for j in range (len(tweetwords)):
    	#print tweetwords[j]
        c.execute("SELECT valence FROM `anew` WHERE `word`='"+tweetwords[j]+"'")
        resultadoanew=c.fetchall()
        
        if len(resultadoanew)==0:
        	anew=0
        else:
        	contval=contval+1
        	for an in resultadoanew:
        		anew=float(an[0])
        		val=anew+val
        		#print tweetwords[j]
    if contval==1:
    	valence=0
        #print "sin valence"
    else:
    	valence=float(val/(contval-1))    
    	#print "valence "+str(valence)+ " por " +str(contval-1)+ " palabras"

	#if valence == 0:
	#	print "este tweet no cae dentro de anew"
    
###  FIN ANEW ###



    ##### EVALUO EN LA RED DE POSITIVOS #######	
    distancia=0
    pares=1
    
    for i in range (len(tweetwords)):
	if "@" in tweetwords[i]:
		tweetwords[i]="<MENCION>"
	if "#" in tweetwords[i]:
		tweetwords[i]="<HASHTAG>"
	if "www" in tweetwords[i] or "http" in tweetwords[i]:
		tweetwords[i]="<URL>"
	if "$" in tweetwords[i]:
		tweetwords[i]="<MONEDA>"
	if tweetwords[i].isdigit():
		tweetwords[i]="<NUMERO>"
    
    for leaf in leaves:
	for i in range (len(tweetwords)):
		if tweetwords[i][-len(leaf):] == leaf:
			tweetwords[i]=tweetwords[i][:-len(leaf)]

    #print "______EVALUO EN POSITIVOS________"
    #print "palabras del tweet a evaluar: "+ str(len(tweetwords))

    for k in range (len(tweetwords)-1):
        #print "Palabras " + str(tweetwords[k])+" y "+str(tweetwords[k+1]) +" en +"
        
        if tweetwords[k] in nodes and tweetwords[k+1] in nodes:
            pares=pares+1
            #print str(tweetwords[k]) +" y "+str(tweetwords[k+1])  + " Estan presentes en G+"
            try:
                if analisis==0:
                        dis=nx.shortest_path_length(g,source=tweetwords[k],target=tweetwords[k+1])
                if analisis==1:
                	dis=nx.shortest_path_length(g,source=tweetwords[k],target=tweetwords[k+1],weight='weight')
                #print "G Pos " + str(dis)
                distancia=distancia+dis
            except nx.NetworkXNoPath, e:
                dis=0
                #print dis
                #print "Entre "+ str(tweetwords[k])+" y "+str(tweetwords[k+1])+" no hay camino."
                    
    
    #print "______RESULTADO POSITIVOS________"

    #print "La suma de distancias es "+ str(distancia)
    #print "Hubo "+ str(pares) + " pares"
    #print "En promedio la distancia es "+ str(distancia/pares) 
    parespos=float(pares)
    #print "parespos: "+str(parespos)
    dispos=float(distancia)
    promdispos=float((dispos/parespos)*float(ponderadis))
    #print "promdispos"+str(promdispos)
    #print "parespos"+str(parespos)
    #print "emopos "+str(emoticonpos)
    costopos=((promdispos)/(parespos**float(ponderapares))) - (emoticonpos)
    if valence > 5:
    	#print contval
    	#print "ayuda valence positivo: "+ str((valence-5)*(contval-1)/1000)
    	costopos=costopos-((valence-5)*(contval-1)/1000)

    ##### EVALUO EN LA RED DE NEGATIVOS #######
    distancia=0
    pares=1
    #print "______EVALUO EN NEGATIVOS________"


    for k in range (len(tweetwords)-1):
        #print "Palabras " + str(tweetwords[k])+" y "+str(tweetwords[k+1]) +" en -"
        
        if tweetwords[k] in nodes2 and tweetwords[k+1] in nodes2:
            #print str(tweetwords[k]) +" y "+str(tweetwords[k+1])  + " Estan presentes en G-"
            pares=pares+1
            try:
                if analisis==0:
                	dis=nx.shortest_path_length(h,source=tweetwords[k],target=tweetwords[k+1])
                if analisis==1:
                	dis=nx.shortest_path_length(h,source=tweetwords[k],target=tweetwords[k+1],weight='weight')
                #print "G Neg " + str(dis)
                distancia=distancia+dis
            except nx.NetworkXNoPath, e:
                dis=0
                #print dis
                #print "Entre "+ str(tweetwords[k])+" y "+str(tweetwords[k+1])+" no hay camino."

    #print "______RESULTADO NEGATIVOS________"

    #print "La suma de distancias es "+ str(distancia)
    #print "Hubo "+ str(pares) + " pares"
    #print "En promedio la distancia es "+ str(distancia/pares) 
    paresneg=float(pares)
    #print "paresneg: "+str(paresneg)
    disneg=float(distancia)
    promdisneg=float((disneg/paresneg)*float(ponderadis))
    #print "emoneg "+str(emoticonneg)
    costoneg=((promdisneg)/(paresneg**float(ponderapares))) - (emoticonneg)
    if valence > 0 and valence < 4:
    #   print valence
    #	print "este tweet podria ser negativo"
    #	print "ayuda valence negativo: "+ str((4-valence)*(contval-1)/1000)
    	costoneg=costoneg-((4-valence)*(contval-1)/1000)
    
    ##### EVALUO EN LA RED DE NEUTROS #######
    distancia=0
    pares=1
    #print "______EVALUO EN NEUTROS________"


    for k in range (len(tweetwords)-1):
        #print "Palabras " + str(tweetwords[k])+" y "+str(tweetwords[k+1]) +" en -o-"
        
        if tweetwords[k] in nodes3 and tweetwords[k+1] in nodes3:
            #print str(tweetwords[k]) +" y "+str(tweetwords[k+1])  + " Estan presentes en Go"
            pares=pares+1
            try:
                #print "Distancia entre " + str(tweetwords[k])+" -> "+str(tweetwords[k+1])
                if analisis==0:
                	dis=nx.shortest_path_length(nt,source=tweetwords[k],target=tweetwords[k+1])
                if analisis==1:
                	dis=nx.shortest_path_length(nt,source=tweetwords[k],target=tweetwords[k+1],weight='weight')
                
                #print "G Neu " + str(dis)
                distancia=distancia+dis
            except nx.NetworkXNoPath, e:
                dis=0
                #print dis
                #print "Entre "+ str(tweetwords[k])+" y "+str(tweetwords[k+1])+" no hay camino."

    #print "______RESULTADO NEUTROS________"

    #print "La suma de distancias es "+ str(distancia)
    #print "Hubo "+ str(pares) + " pares"
    #print "En promedio la distancia es "+ str(distancia/pares) 
    paresneu=float(pares)
    #print "paresneu: "+str(paresneu)
    disneu=float(distancia)
    promdisneu=float((disneu/paresneu)*float(ponderadis))
    costoneu=(promdisneu)/paresneu**float(ponderapares)
    
    
    #print "______RESULTADO FINAL________"
    #print "pares+: "+str(parespos)+ " vs pares-:"+str(paresneg)
    #print "dist: "+str(dispos)+ " vs "+str(disneg)
    #print "Promdist +: "+str(float(promdispos))+ " vs Promdist -:"+str(float(promdisneg))
    
    #print "Costo de produccion: [+] ->"+str(costopos)+ " [-] ->"+str(costoneg)+ " [o] ->"+str(costoneu)
    
    #############################################################
    #########################DECISION############################
    #############################################################

  
    #### DECISION POR PARES
    
    if parespos == 1 and paresneu == 1 and paresneg > 1:
    	#print "el tweet es Negativo"
    	c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='2' WHERE `id_articulo`='"+str(id)+"'")
    
    if paresneg == 1 and paresneu == 1 and parespos > 1:
    	#print "el tweet es Positivo"
    	c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='1' WHERE `id_articulo`='"+str(id)+"'")
    
    if paresneg == 1 and parespos == 1 and paresneu > 1:
    	#print "el tweet es Neutro"
    	c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")
    
    if parespos == 1 and paresneg == 1 and paresneu == 1:
    	#print "el tweet es no se puede clasificar"
    	c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='5' WHERE `id_articulo`='"+str(id)+"'")
    
    #### DECISION POR COSTO DE PRODUCCION
    if parespos > 1 and paresneg > 1 and paresneu > 1:
    
    	if costopos > costoneg and costoneu > costoneg:
    		#print "El Tweet es negativo"
    		c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='2' WHERE `id_articulo`='"+str(id)+"'")
    	if costopos < costoneg and costopos < costoneu:
    		#print "El Tweet es positivo"
    		c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='1' WHERE `id_articulo`='"+str(id)+"'")
    	
    	if costoneu < costoneg and costoneu < costopos:
    		#print "El Tweet es neutro"
    		c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")
    
    #### DECISION POR COSTOS SIMILARES	
    	if costopos < costoneu and costoneg < costoneu:
    		if costopos == costoneg:
    			#print "El Tweet es neutro"
    			c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")
    	
    	if costopos < costoneg and costoneu < costoneg:
    		if costopos == costoneu:
    			#print "El Tweet es neutro"
    			c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")
    	
    	if costoneg < costopos and costoneu < costopos:
    		if costoneg == costoneu:
    			#print "El Tweet es neutro"
    			c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")
    
    
    if costopos==0:
    	if costoneg==costoneu:
    		#print "El Tweet es neutro"
    		c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='0' WHERE `id_articulo`='"+str(id)+"'") 
    	else:
    		if costoneg>costoneu:
    			#print "El Tweet es neutro"
    			c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='0' WHERE `id_articulo`='"+str(id)+"'") 	
    		else:
    			#print "El Tweet es negativo"
    			c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='2' WHERE `id_articulo`='"+str(id)+"'") 	
    
    
    if costoneg==0:
    	if costopos==costoneu:
    		#print "El Tweet es neutro"
    		c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='0' WHERE `id_articulo`='"+str(id)+"'") 
    	else:
    		if costopos>costoneu:
    			#print "El Tweet es neutro"
    			c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='0' WHERE `id_articulo`='"+str(id)+"'") 	
    		else:
    			#print "El Tweet es positivo"
    			c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='1' WHERE `id_articulo`='"+str(id)+"'")
    
    if costoneu==0:
    	if costopos==costoneg:
    		#print "El Tweet es neutro"
    		c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='0' WHERE `id_articulo`='"+str(id)+"'") 
    	else:
    		if costopos>costoneg:
    			#print "El Tweet es negativo"
    			c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='2' WHERE `id_articulo`='"+str(id)+"'") 	
    		else:
    			#print "El Tweet es positivo"
    			c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='1' WHERE `id_articulo`='"+str(id)+"'")
    
    
    if costoneu==0 and costoneg==0 and costopos>0:
    	#print "el tweet es positivo"
    	c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='1' WHERE `id_articulo`='"+str(id)+"'")
    
    
    if costoneu==0 and costopos==0 and costoneg>0:
    	#print "el tweet es negativo"
    	c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='2' WHERE `id_articulo`='"+str(id)+"'")
    
    if costoneg==0 and costopos==0 and costoneu>0:
    	#print "el tweet es neutro"
    	c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")
    
    
    
    if costoneu==0 and costopos==0 and costoneg==0:
    	#print "el tweet es no se puede clasificar"
    	c.execute("UPDATE `clasificar_"+str(tabla)+"` SET `"+str(w)+"`='5' WHERE `id_articulo`='"+str(id)+"'")
    	
    ##print "_____________________________________________"		

    tweet=[]
    db.commit()


####CALCULOS FINALES####
c.execute("SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `"+str(w)+"`!= 5")
consulta=c.fetchall()
for reg in consulta:
	#print "Tweets totales evaluados: "+str(reg[0])
	Total=reg[0]
	

c.execute("SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `"+str(w)+"`= 5")
consulta=c.fetchall()
for reg in consulta:
	sineva=reg[0]

print "Tweets sin clasificar: "+str((float(sineva)/float(Total))*100)+"%" +", "+ str(sineva) + " de " + str(Total)

TP_u=0
FP_u=0
FN_u=0

#print "PERFORMANCE"	
#neutros
print "Neutros"
#f.write("\n_*_*_*_*_*_*_*_*_*_*\n")
#f.write("Neutros \n")

c.execute("SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=0 and `"+str(w)+"`= 0 AND `"+str(w)+"`!= 5 ")
consulta=c.fetchall()

for reg in consulta:
	#print "TPn: "+str(reg[0])
	TPn=float(reg[0])
	TP_u=TP_u+TPn

c.execute("SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`!= 0 and `"+str(w)+"`= 0 AND `"+str(w)+"`!= 5 ")
consulta=c.fetchall()

for reg in consulta:
	#print "FPn: "+str(reg[0])
	FPn=float(reg[0])
	FP_u=FP_u+FPn
	
c.execute("SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=0 and `"+str(w)+"`!=0 AND `"+str(w)+"`!= 5 ")
consulta=c.fetchall()

for reg in consulta:
	#print "FNn: "+str(reg[0])
	FNn=float(reg[0])
	FN_u=FN_u+FNn
	
#print "TNn: "+str(Total-(TPn+FPn+FNn))
TNn=float(Total-(TPn+FPn+FNn))

#print "_*_*_*_*_*_*_*_*_*_*"
if (TPn+FPn+FNn+TNn) !=0:
	accun=float((TPn+TNn)/(TPn+FPn+FNn+TNn))
	#print "Accuracy: " + str(accun)
else:
	#print "Accuracy: No definido (/0)"
	accun=0

if (TPn+FPn) !=0:
	pren=float((TPn)/(TPn+FPn))	
	print "Precission: " + str(pren)
else:
	#print "Precission: No definido (/0)"
	pren=0

if (TPn+FNn) !=0:
	recn=float((TPn)/(TPn+FNn))
	print "Recall: " + str(recn)
else:
	#print "Recall: No definido (/0)"
	recn=0
#try:
#    print "F-1: "+str( 2*pren*recn/(pren+recn) )
#    f.write("F-1: "+str( 2*pren*recn/(pren+recn) ))
#except:
#    pass
print "_*_*_*_*_*_*_*_*_*_*"
#f.write("\n_*_*_*_*_*_*_*_*_*_*\n")

#positivos
print "Positivos"
#f.write("Positivos\n")

c.execute("SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=1 and `"+str(w)+"`= 1 AND `"+str(w)+"`!= 5 ")
consulta=c.fetchall()

for reg in consulta:
	#print "TPp: "+str(reg[0])
	TPp=float(reg[0])
	TP_u=TP_u+TPp

c.execute("SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`!= 1 and `"+str(w)+"`= 1 AND `"+str(w)+"`!= 5 ")
consulta=c.fetchall()

for reg in consulta:
	#print "FPp: "+str(reg[0])
	FPp=float(reg[0])
	FP_u=FP_u+FPp
c.execute("SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=1 and `"+str(w)+"`!=1 AND `"+str(w)+"`!= 5 ")
consulta=c.fetchall()

for reg in consulta:
	#print "FNp: "+str(reg[0])
	FNp=float(reg[0])
	FN_u=FN_u+FNp
	
#print "TNp: "+str(Total-(TPp+FPp+FNp))
TNp=float(Total-(TPp+FPp+FNp))


#print "_*_*_*_*_*_*_*_*_*_*"
if (TPp+FPp+FNp+TNp) !=0:
	accup=float((TPp+TNp)/(TPp+FPp+FNp+TNp))
	#print "Accuracy: " + str(accup)
else:
	#print "Accuracy: No definido (/0)"
	accup=0

if (TPp+FPp) !=0:	
	prep=float((TPp)/(TPp+FPp))
	print "Precission: " + str(prep)
else:
	#print "Precission: No definido (/0)"
	prep=0

if (TPp+FNp) !=0:
	recp=float((TPp)/(TPp+FNp))
	print "Recall: " + str(recp)
else:
	#print "Recall: No definido (/0)"
	recp=0
#try:
#    print "F-1: "+str( 2*prep*recp/(prep+recp) )
#    #f.write("F-1: "+str( 2*prep*recp/(prep+recp) ))
#except:
#    pass
print "_*_*_*_*_*_*_*_*_*_*"
#f.write("\n_*_*_*_*_*_*_*_*_*_*\n")
#NEGATIVOS

print "Negativos"
#f.write("Negativos\n")
c.execute("SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=2 and `"+str(w)+"`= 2 AND `"+str(w)+"`!= 5 ")
consulta=c.fetchall()

for reg in consulta:
	#print "TPng: "+str(reg[0])
	TPng=float(reg[0])
	TP_u=TP_u+TPng

c.execute("SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`!= 2 and `"+str(w)+"`= 2 AND `"+str(w)+"`!= 5 ")
consulta=c.fetchall()

for reg in consulta:
	#print "FPng: "+str(reg[0])
	FPng=float(reg[0])
	FP_u=FP_u+FPng
	
c.execute("SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=2 and `"+str(w)+"`!=2 AND `"+str(w)+"`!= 5 ")
consulta=c.fetchall()

for reg in consulta:
	#print "FNng: "+str(reg[0])
	FNng=float(reg[0])
	FN_u=FN_u+FNng
	
#print "TNng: "+str(Total-(TPng+FPng+FNng))
TNng=float(Total-(TPng+FPng+FNng))

#print "_*_*_*_*_*_*_*_*_*_*"
if (TPng+FPng+FNng+TNng) !=0:
	accung=float((TPng+TNng)/(TPng+FPng+FNng+TNng))
	#print "Accuracy: " + str(accung)
else:
	#print "Accuracy: No definido (/0)"
	accung=0

if (TPng+FPng) !=0:	
	preng=float((TPng)/(TPng+FPng))
	print "Precission: " + str(preng)
else:
	#print "Precission: No definido (/0)"
	preng=0

if (TPng+FNng) !=0:
	recng=float((TPng)/(TPng+FNng))
	print "Recall: " + str(recng)
else:
	#print "Recall: No definido (/0)"
	recng=0
#try:
#    print "F-1: "+str( 2*preng*recng/(preng+recng) )
#    #f.write("F-1: "+str( 2*preng*recng/(preng+recng) ))
#except:
#    pass
#print "_*_*_*_*_*_*_*_*_*_*"

print "_*_*_*_*_*_*"
print "microaverage"
print "_*_*_*_*_*_*"

#print str(TP_u)+" kkakaka"
#print str(FP_u)+" kkakaka"
#print str(FN_u)+" kkakaka"

print "Precision: " + str(float(TP_u/(TP_u+FP_u)))
microPRE=float(TP_u/(TP_u+FP_u))
print "Recall: " + str(float(TP_u/(TP_u+FN_u)))
microREC=float(TP_u/(TP_u+FN_u))
print "F-measure: " + str(2*microPRE*microREC/(microPRE+microREC))
print "_*_*_*_*_*_*"
print "MACROaverage"
print "_*_*_*_*_*_*"

print "Precision: " + str(float(pren+prep+preng)/3)
MACROPRE=float((pren+prep+preng)/3)
print "Recall: " + str(float(recn+recp+recng)/3)
MACROREC=float((recn+recp+recng)/3)
print "F-measure: " + str(2*MACROPRE*MACROREC/(MACROPRE+MACROREC))


db.close()