import sys
import rrdtool
import time
tiempo_actual = int(time.time())
#Grafica desde el tiempo actual menos diez minutos
tiempo_inicial = tiempo_actual - 1000

ret = rrdtool.graphv("pack_uni.png",
                      "--start", str(tiempo_inicial),
                      "--end", "N",
                      "--vertical-label=Paquetes",
                      "--title=Paquetes unicast que\nha recibido la interfaz", 
                      "DEF:pEntrada=segmentosRed.rrd:paquetesUnicast:AVERAGE",
                      "VDEF:paqEntradaLast=pEntrada,LAST",
                      "VDEF:paqEntradaFirst=pEntrada,FIRST",
                      "VDEF:paqEntradaMax=pEntrada,MAXIMUM",
                      "VDEF:paqEntradaDev=pEntrada,STDEV",
                      "CDEF:Nivel1=pEntrada,7,GT,0,pEntrada,IF",
                      "PRINT:paqEntradaLast:%6.2lf",
                      "PRINT:paqEntradaFirst:%6.2lf",
                      "GPRINT:paqEntradaMax:%6.2lf %S pEntMAX",
                      "GPRINT:paqEntradaDev:%6.2lf %S STDEV",
                      "LINE3:pEntrada#FF0000:Paquetes recibidos"
)
ret = rrdtool.graphv("pack_ipv4.png",
                      "--start", str(tiempo_inicial),
                      "--end", "N",
                      "--vertical-label=Paquetes",
                      "--title=Paquetes recibidos a\nprotocolos IPv4 (errores tmb)", 
                      "DEF:pEntrada=segmentosRed.rrd:paquetesIPv4:AVERAGE",
                      "VDEF:paqEntradaLast=pEntrada,LAST",
                      "VDEF:paqEntradaFirst=pEntrada,FIRST",
                      "VDEF:paqEntradaMax=pEntrada,MAXIMUM",
                      "VDEF:paqEntradaDev=pEntrada,STDEV",
                      "CDEF:Nivel1=pEntrada,7,GT,0,pEntrada,IF",
                      "PRINT:paqEntradaLast:%6.2lf",
                      "PRINT:paqEntradaFirst:%6.2lf",
                      "GPRINT:paqEntradaMax:%6.2lf %S pEntMAX",
                      "GPRINT:paqEntradaDev:%6.2lf %S STDEV",
                      "LINE3:pEntrada#00FF00:Paquetes recibidos"
)
ret = rrdtool.graphv("msjs_ICMP.png",
                      "--start", str(tiempo_inicial),
                      "--end", "N",
                      "--vertical-label=Mensajes",
                      "--title=Mensajes ICMPecho enviados", 
                      "DEF:pEntrada=segmentosRed.rrd:paquetesICMPecho:AVERAGE",
                      "VDEF:paqEntradaLast=pEntrada,LAST",
                      "VDEF:paqEntradaFirst=pEntrada,FIRST",
                      "VDEF:paqEntradaMax=pEntrada,MAXIMUM",
                      "VDEF:paqEntradaDev=pEntrada,STDEV",
                      "CDEF:Nivel1=pEntrada,7,GT,0,pEntrada,IF",
                      "PRINT:paqEntradaLast:%6.2lf",
                      "PRINT:paqEntradaFirst:%6.2lf",
                      "GPRINT:paqEntradaMax:%6.2lf %S pEntMAX",
                      "GPRINT:paqEntradaDev:%6.2lf %S STDEV",
                      "LINE3:pEntrada#0000FF:Mensajes ICMPecho recibidos"
)
ret = rrdtool.graphv("segmentos_entrada.png",
                      "--start", str(tiempo_inicial),
                      "--end", "N",
                      "--vertical-label=Segmentos",
                      "--title=Segmentos recibidos (errores tmb)", 
                      "DEF:pEntrada=segmentosRed.rrd:segmentosEntrada:AVERAGE",
                      "VDEF:paqEntradaLast=pEntrada,LAST",
                      "VDEF:paqEntradaFirst=pEntrada,FIRST",
                      "VDEF:paqEntradaMax=pEntrada,MAXIMUM",
                      "VDEF:paqEntradaDev=pEntrada,STDEV",
                      "CDEF:Nivel1=pEntrada,7,GT,0,pEntrada,IF",
                      "PRINT:paqEntradaLast:%6.2lf",
                      "PRINT:paqEntradaFirst:%6.2lf",
                      "GPRINT:paqEntradaMax:%6.2lf %S pEntMAX",
                      "GPRINT:paqEntradaDev:%6.2lf %S STDEV",
                      "LINE3:pEntrada#00FFFF:Segmentos"
)
ret = rrdtool.graphv("datagramas_UDP.png",
                      "--start", str(tiempo_inicial),
                      "--end", "N",
                      "--vertical-label=Datagramas",
                      "--title=Datagramas entregados a usuarios UDP", 
                      "DEF:pEntrada=segmentosRed.rrd:datagramasSalida:AVERAGE",
                      "VDEF:paqEntradaLast=pEntrada,LAST",
                      "VDEF:paqEntradaFirst=pEntrada,FIRST",
                      "VDEF:paqEntradaMax=pEntrada,MAXIMUM",
                      "VDEF:paqEntradaDev=pEntrada,STDEV",
                      "CDEF:Nivel1=pEntrada,7,GT,0,pEntrada,IF",
                      "PRINT:paqEntradaLast:%6.2lf",
                      "PRINT:paqEntradaFirst:%6.2lf",
                      "GPRINT:paqEntradaMax:%6.2lf %S pEntMAX",
                      "GPRINT:paqEntradaDev:%6.2lf %S STDEV",
                      "LINE3:pEntrada#FF00FF:Datagramas"
)

# ret = rrdtool.graphv( "segmentosTCP.png",
#                      "--start",str(tiempo_inicial),
#                      "--end","N",
#                      "--vertical-label=Segmentos",
#                      "--title=Segmentos TCP de un agente \n Usando SNMP y RRDtools",
#                      "DEF:sEntrada=segmentosRed.rrd:segmentosEntrada:AVERAGE",
#                      "DEF:sSalida=segmentosRed.rrd:segmentosSalida:AVERAGE",
#                       "VDEF:segEntradaLast=sEntrada,LAST",
#                       "VDEF:segEntradaFirst=sEntrada,FIRST",
#                       "VDEF:segEntradaMax=sEntrada,MAXIMUM",
#                       "VDEF:segEntradaDev=sEntrada,STDEV",
#                       "CDEF:Nivel1=sEntrada,7,GT,0,sEntrada,IF",
#                       "PRINT:segEntradaLast:%6.2lf",
#                       "PRINT:segEntradaFirst:%6.2lf",
#                      "GPRINT:segEntradaMax:%6.2lf %S segEntMAX",
#                      "GPRINT:segEntradaDev:%6.2lf %S STDEV",
#                      "LINE3:sEntrada#FF0000:Segmentros recibidos",
#                      "LINE3:sSalida#0000FF:Segmentos enviados" )
print(ret)