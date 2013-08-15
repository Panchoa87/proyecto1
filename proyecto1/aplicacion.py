'''
Created on 30/07/2013

@author: Pancho
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
    if w=="netsense_w":
        analisis=1
    if w=="netsense":
        analisis=0
    #bd=entrena.entrenamiento("0",tabla,1000)
    #sys.exit(0)
    inicio = time.time()
    
    neutro = r.red(0,stpw,balance,umbralpeso)
    positivo = r.red(1,stpw,balance,umbralpeso)
    negativo = r.red(2,stpw,balance,umbralpeso)
    resultado=result.resultado(tabla,w)
    
    nodos=[]
    nodos.append(neutro.getNumeroNodos())
    nodos.append(positivo.getNumeroNodos())
    nodos.append(negativo.getNumeroNodos())
    maximo = sorted(nodos)
    neutro.setBalance(maximo[2])
    positivo.setBalance(maximo[2])
    negativo.setBalance(maximo[2])
    
    conn=conex.conexion()
    sql=" SELECT cuerpo,id_articulo FROM `clasificar_"+str(tabla)+"` "
    conn.ejecutarSql(sql)
    resultadotweet=conn.getResultado()
    tiempo=0
    for regtweet in resultadotweet:
        inicioTweet=time.time()
        cuerpo=regtweet[0]
        id=str(regtweet[1])
        tweetEvaluar=evaluar.tweet(cuerpo,stpw)
        palabrasTweet=tweetEvaluar.getPalabrasTweet()
        
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
    resultado.estadisticas()
    print "Tiempo Promedio por tweet: ",tiempo/len(resultadotweet),"s"
    num=time.time()-inicio
    minu=int(num/60)  
    seg=(num-(minu*60))  
    print "Tiempo Total de ejecucion: ",str(minu)+"m "+str(seg),"s"
        