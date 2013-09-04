'''
Created on 27-08-2013

@author: pancho
'''
#0 neutro
#1 positivo
#2 negativo
import sys
import red as r
import tweet as evaluar
import evaluacion as ev
import conexion as conex
import resultado as result
import entrenamiento as entrena
import time

if __name__ == '__main__':
    
    tabla=str(sys.argv[1])
    w=str(sys.argv[2])
    stpw=str(sys.argv[3])
    balance=str(sys.argv[4])
    ponderapares=sys.argv[5]
    ponderadis=sys.argv[6]
    umbralpeso=sys.argv[7]
    validacion=int(sys.argv[8])
    if w=="netsense_w":
        analisis=1
    if w=="netsense":
        analisis=0
        
    raw_input("Press enter to continue")
    #ver la cantidad de elementos del intervalo
    conn=conex.conexion()
    sql=" SELECT count(*) FROM `clasificar_"+str(tabla)+"` "
    conn.ejecutarSql(sql)
    minimo=0
    intervalo=conn.getResultado()
    intervalo=intervalo[0][0]
    int=intervalo/validacion
    rest=intervalo % validacion
    resultados=[]
    inicio = time.time()
    for i in range(0,validacion):
        ides=""
        #Saco los tweets de prueba
        sql="SELECT id_articulo FROM `clasificar_"+str(tabla)+"` LIMIT "+str(minimo)+","+str(int)+""
        conn.ejecutarSql(sql)
        resultado=conn.getResultado()
        for registro in resultado:
            ides=str(ides)+str(registro[0])+","
        ides=str(ides[0:len(ides)-1])
        entrena.entrenamiento(tabla,balance,stpw,ides)
        
        #creo las redes de palabras
        neutro = r.red(0,stpw,balance,umbralpeso)
        positivo = r.red(1,stpw,balance,umbralpeso)
        negativo = r.red(2,stpw,balance,umbralpeso)
        
        nodos=[]
        nodos.append(neutro.getNumeroNodos())
        nodos.append(positivo.getNumeroNodos())
        nodos.append(negativo.getNumeroNodos())
        print "------------------------------------------------"
        print "nodos neutros:"+str(neutro.getNumeroNodos())
        print "enlaces neutros"+str(neutro.getNumeroEnlaces())
        print "nodos positivos:"+str(positivo.getNumeroNodos())
        print "enlaces positivos"+str(positivo.getNumeroEnlaces())
        print "nodos negativos:"+str(negativo.getNumeroNodos())
        print "enlaces negativos"+str(negativo.getNumeroEnlaces())
        print "------------------------------------------------"
        maximo = sorted(nodos)
        neutro.setBalance(maximo[2])
        positivo.setBalance(maximo[2])
        negativo.setBalance(maximo[2])
        sql=" SELECT cuerpo,id_articulo FROM `clasificar_"+str(tabla)+"` where id_articulo IN ("+ides+")"
        resultado=result.resultado(tabla,w)
        conn.ejecutarSql(sql)
        resultadotweet=conn.getResultado()
        tiempo=0
        for regtweet in resultadotweet:
            inicioTweet=time.time()
            cuerpo=regtweet[0]
            id=str(regtweet[1])
            #print cuerpo
            tweetEvaluar=evaluar.tweet(cuerpo,stpw)
            palabrasTweet=tweetEvaluar.getPalabrasTweet()
            #print palabrasTweet
            
            evaluacionNeutro=ev.evaluacion(palabrasTweet,neutro,0,analisis,ponderadis,ponderapares)
            #evaluacionNeutro.debug("neutro")
            
            evaluacionPositivo=ev.evaluacion(palabrasTweet,positivo,tweetEvaluar.getEmoticonPos(),analisis,ponderadis,ponderapares)
            #evaluacionPositivo.debug("positivo")
            
            if tweetEvaluar.getValencia() > 5:
                #print contval
                #print "ayuda valence positivo: "+ str((valence-5)*(contval-1)/1000)
                costo=evaluacionPositivo.getCosto()-((tweetEvaluar.getValencia()-5)*(tweetEvaluar.getContVal()-1)/1000)
                evaluacionPositivo.setCosto(costo)
            
            evaluacionNegativo=ev.evaluacion(palabrasTweet,negativo,tweetEvaluar.getEmoticonNeg(),analisis,ponderadis,ponderapares)
            #evaluacionNegativo.debug("negativo")
            
            if tweetEvaluar.getValencia() > 0 and tweetEvaluar.getValencia() < 4  :
                #print contval
                #print "ayuda valence positivo: "+ str((valence-5)*(contval-1)/1000)
                costo=evaluacionNegativo.getCosto()-((4-tweetEvaluar.getValencia())*(tweetEvaluar.getContVal()-1)/1000)
                evaluacionNegativo.setCosto(costo)
            resultado.analizar(id, evaluacionPositivo, evaluacionNeutro, evaluacionNegativo)
            tiempo=tiempo+(time.time()-inicioTweet)
        resultado.estadisticas(ides)
        resultados.append(resultado)
        print "Tiempo Promedio por tweet: ",tiempo/len(resultadotweet),"s"
        print "validacion numero:"+str(i+1)
        minimo=minimo+int
        if(i==validacion-2):
            int=int+rest
    num=time.time()-inicio
    minu=float(num/60)  
    seg=(num-(minu*60))  
    print "Tiempo Total de ejecucion: ",str(minu)+"m "+str(seg),"s"
    print "---------------------------------------\n"
    print "Resultados Finales"
    pren=0
    ren=0
    prepos=0
    repos=0
    preneg=0
    reneg=0
    premacro=0
    remacro=0
    f1macro=0
    premicro=0
    remicro=0
    f1micro=0
    for i in resultados:
        pren=i.getPrecisionNeutros()+pren
        ren=ren+i.getRecallNeutros()
        prepos=i.getPrecisionPositivos()+prepos
        repos=repos+i.getRecallPositivos()
        preneg=i.getPrecisionNegativos()+preneg
        reneg=reneg+i.getRecallNegativos()
        premacro=premacro+i.getMacroPrecision()
        remacro=remacro+i.getMacroRec()
        f1macro=f1macro+i.getMacroF1()
        premicro=premicro+i.getMicroPrecision()
        remicro=remicro+i.getMicroRec()
        f1micro=f1micro+i.getMicroF1()
    print "Promedio precision Neutros: "+str(pren/validacion)
    print "Promedio recall Neutros: "+str(ren/validacion)
    print "Promedio precision Positivos: "+str(prepos/validacion)
    print "Promedio recall Positivos: "+str(repos/validacion)
    print "Promedio precision Negativos: "+str(preneg/validacion)
    print "Promedio recall Negativos: "+str(reneg/validacion)
    print "Promedio Precision Macro: "+str(premacro/validacion)
    print "Promedio Recall Macro: "+str(remacro/validacion)
    print "Promedio F1 Macro: "+str(f1macro/validacion)
    print "Promedio Precision Micro: "+str(premicro/validacion)
    print "Promedio Recall Micro: "+str(remicro/validacion)
    print "Promedio F1 Macro: "+str(f1micro/validacion)
    fila=""
    print " c | b | a "
    sql="SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=0 and `"+str(w)+"`= 2 AND `"+str(w)+"`!= 5 "   
    conn.ejecutarSql(sql)
    consulta=conn.getResultado()
    for reg in consulta:
        aux=float(reg[0])
    fila=fila+str(aux)+"|"
    sql="SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=0 and `"+str(w)+"`= 1 AND `"+str(w)+"`!= 5 "   
    conn.ejecutarSql(sql)
    consulta=conn.getResultado()
    for reg in consulta:
        aux=float(reg[0])
    fila=fila+str(aux)+"|"
    sql="SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=0 and `"+str(w)+"`= 0 AND `"+str(w)+"`!= 5 "   
    conn.ejecutarSql(sql)
    consulta=conn.getResultado()
    for reg in consulta:
        aux=float(reg[0])
    print fila+str(aux)+"| a= neutro"
    fila=""
    sql="SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=1 and `"+str(w)+"`= 2 AND `"+str(w)+"`!= 5 "   
    conn.ejecutarSql(sql)
    consulta=conn.getResultado()
    for reg in consulta:
        aux=float(reg[0])
    fila=fila+str(aux)+"|"
    sql="SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=1 and `"+str(w)+"`= 1 AND `"+str(w)+"`!= 5 "   
    conn.ejecutarSql(sql)
    consulta=conn.getResultado()
    for reg in consulta:
        aux=float(reg[0])
    fila=fila+str(aux)+"|"
    sql="SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=1 and `"+str(w)+"`= 0 AND `"+str(w)+"`!= 5 "   
    conn.ejecutarSql(sql)
    consulta=conn.getResultado()
    for reg in consulta:
        aux=float(reg[0])
    print fila+str(aux)+"| b= positivo" 
    fila=""
    sql="SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=2 and `"+str(w)+"`= 2 AND `"+str(w)+"`!= 5 "   
    conn.ejecutarSql(sql)
    consulta=conn.getResultado()
    for reg in consulta:
        aux=float(reg[0])
    fila=fila+str(aux)+"|"
    sql="SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=2 and `"+str(w)+"`= 1 AND `"+str(w)+"`!= 5 "   
    conn.ejecutarSql(sql)
    consulta=conn.getResultado()
    for reg in consulta:
        aux=float(reg[0])
    fila=fila+str(aux)+"|"
    sql="SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `sentido_manual`=2 and `"+str(w)+"`= 0 AND `"+str(w)+"`!= 5 "   
    conn.ejecutarSql(sql)
    consulta=conn.getResultado()
    for reg in consulta:
        aux=float(reg[0])
    print fila+str(aux)+"| c= negativo"
    sql="SELECT COUNT(*) FROM `clasificar_"+str(tabla)+"` WHERE `"+str(w)+"`= 5 "   
    conn.ejecutarSql(sql)
    consulta=conn.getResultado()
    for reg in consulta:
        aux=float(reg[0]) 
    print "tweets sin clasificar: "+str(aux)           