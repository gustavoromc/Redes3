import sys
import rrdtool
import time
import datetime
from  Notify import send_alert_attached
import time
rrdpath = './rrd/'
imgpath = './img/'

last_value = int(rrdtool.last(rrdpath + "trend.rrd"))
last_time = last_value
initial_time = last_time - 1800

def generarGrafica(last_value, dato, titulo, u1, u2, u3):
    tiempo_final = int(last_value)
    tiempo_inicial = tiempo_final - 1800
    ret = rrdtool.graphv(imgpath + titulo + ".png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Cpu load",
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                    "--title=Carga del " + titulo,
                    "DEF:carga="+rrdpath+"trend.rrd:" + dato + ":AVERAGE",
                     "VDEF:cargaMAX=carga,MAXIMUM",
                     "VDEF:cargaMIN=carga,MINIMUM",
                     "VDEF:cargaSTDEV=carga,STDEV",
                     "VDEF:cargaLAST=carga,LAST",
                     "CDEF:umbral" + u1 + "=carga," + u1 + ",LT,0,carga,IF",
                     "CDEF:umbral" + u2 + "=carga," + u2 + ",LT,0,carga,IF",
                     "CDEF:umbral" + u3 + "=carga," + u3 + ",LT,0,carga,IF",
                     "AREA:carga#00FF00:Carga de " + titulo,
                     "AREA:umbral" + u1 + "#00FF00:Carga " + titulo + "mayor de " + u1 + "",
                     "AREA:umbral" + u2 + "#FF7A00:Carga " + titulo + "mayor de " + u2 + "",
                     "AREA:umbral" + u3 + "#FF0000:Carga " + titulo + "mayor de " + u3 + "",
                     "HRULE:" + u1 + "#00FF00:Umbral  " + u1 + "%",
                     "HRULE:" + u2 + "#FF7A00:Umbral  " + u1 + "%",
                     "HRULE:" + u3 + "#FF0000:Umbral  " + u1 + "%",
                     "PRINT:cargaLAST:%6.2lf",
                     "GPRINT:cargaMIN:%6.2lf %SMIN",
                     "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                     "GPRINT:cargaLAST:%6.2lf %SLAST" )
    #print (ret)

pathImage = imgpath + "useCPU.png"
envioCPU30 = True
envioCPU75 = True
envioCPU80 = True

envioRAM30 = True
envioRAM80 = True
envioRAM90 = True

envioDisco30 = True
envioDisco70 = True
envioDisco90 = True

while (1):
    ultima_actualizacion = rrdtool.lastupdate(rrdpath + "trend.rrd")
    timestamp=ultima_actualizacion['date'].timestamp()
    datoCPU=ultima_actualizacion['ds']["CPUload"]
    datoRAM=ultima_actualizacion['ds']["RAMload"]
    datoDisco=ultima_actualizacion['ds']["DISKload"]
    #print(datoCPU)
    #print(datoRAM)
    #print(datoDisco)
    
    if datoCPU> 80:
        time.sleep(15)
        if envioCPU80:
            pathImage = imgpath + "CPU.png"
            generarGrafica(int(timestamp),"CPUload","CPU","30","70","90")
            send_alert_attached("A L E R T A: ACTIVIDAD ALTA DE CPU","CPU usage is above 80%, please take action.",pathImage)
            envioCPU80 = False
            print("Enviado")
    elif datoCPU >75 and datoCPU<79:
        if envioCPU75:
            pathImage = imgpath + "CPU.png"
            generarGrafica(int(timestamp),"CPUload","CPU","30","70","90")
            send_alert_attached("A L E R T A: ACTIVIDAD NORMAL DE CPU","CPU usage is above 75%, monitor usage.",pathImage)
            envioCPU75 = False
            print("Enviado")
    elif datoCPU > 30 and datoCPU<74:
        if envioCPU30:
            pathImage = imgpath + "CPU.png"
            generarGrafica(int(timestamp),"CPUload","CPU","30","70","90")
            envioCPU30 = False
            send_alert_attached("A L E R T A: ACTIVIDAD LEVE DE CPU","CPU usage is above 30%, none action is needed",pathImage)
            print("Enviado")
    ########################        RAM         #######################  
    if datoRAM>=80:
        if envioRAM90:
            pathImage = imgpath + "RAM.png"
            generarGrafica(int(timestamp),"RAMload","RAM","30","70","80")
            send_alert_attached("A L E R T A: ACTIVIDAD ALTA DE RAM","RAM usage is above 70%, monitor usage.",pathImage)
            envioRAM90 = False
            print("Enviado")
    elif datoRAM >=70 and datoRAM <=79:
        if envioRAM80:
            pathImage = imgpath + "RAM.png"
            generarGrafica(int(timestamp),"RAMload","RAM","30","70","80")
            send_alert_attached("A L E R T A: ACTIVIDAD NORMAL DE RAM","RAM usage is above 70%, none action is needed.",pathImage)
            envioRAM7 = False
            print("Enviado")
    elif datoRAM >=30 and datoRAM<=69:
        if envioRAM30:
            pathImage = imgpath + "RAM.png"
            generarGrafica(int(timestamp),"RAMload","RAM","30","70","80")
            envioRAM30 = False
            send_alert_attached("A L E R T A: ACTIVIDAD LEVE DE RAM","RAM usage is above 30%.",pathImage)
            print("Enviado")
    ########################        DISK         #######################  
    """if datoDisco> 90 and envioDisco90:
        pathImage = imgpath + "Disco.png"
        generarGrafica(int(timestamp),"DISKload","Disco","30","70","90")
        send_alert_attached("A L E R T A: ACTIVIDAD ALTA DE DISCO","El uso del Disco esta por encima del 90%, favor de tomar las medidas correspondientes.",pathImage)
        envioDisco90 = False
        print("Enviado")
    elif datoDisco >70 and envioDisco70:
        pathImage = imgpath + "Disco.png"
        generarGrafica(int(timestamp),"DISKload","Disco","30","70","90")
        send_alert_attached("A L E R T A: ACTIVIDAD NORMAL DE DISCO","El uso del Disco esta por encima del 70%, favor de monitoriar el uso del Disco.",pathImage)
        envioDisco70 = False
        print("Enviado")
    elif datoDisco > 30 and envioDisco30:
        pathImage = imgpath + "Disco.png"
        generarGrafica(int(timestamp),"DISKload","Disco","30","70","90")
        envioDisco30 = False
        send_alert_attached("A L E R T A: ACTIVIDAD LEVE DE DISCO","El uso del Disco esta por encima del 30%.",pathImage)
        print("Enviado")"""
    time.sleep(15)