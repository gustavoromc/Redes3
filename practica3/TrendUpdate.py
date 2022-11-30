import time
import rrdtool
from getSNMP import consultaSNMP
rrdpath = './rrd/'
carga_CPU = 0
ramTotal = 0
ramUsada = 0
discoTotal = 0
discoUsado = 0
ramPorcentaje = 0
discoPorcentaje = 0

while 1:

    i = 6
    sum = 0
    avg = 0
    while i <= 17:
        carga_CPU = int(consultaSNMP('eduardoCuevas','172.20.10.7','1.3.6.1.2.1.25.3.3.1.2.' + str(i)))
        i = i + 1
        sum = sum + carga_CPU
    # carga_CPU = int(consultaSNMP('comunidadSNMP','172.20.10.7','1.3.6.1.2.1.25.3.3.1.2.196616'))
    avg = sum / 12

    discoTotal = 4096*int(consultaSNMP('eduardoCuevas','172.20.10.7','1.3.6.1.2.1.25.2.3.1.5.1'))
    discoUsado = 4096*int(consultaSNMP('eduardoCuevas','172.20.10.7','1.3.6.1.2.1.25.2.3.1.6.1'))

    ramTotal = 65536*int(consultaSNMP('eduardoCuevas','172.20.10.7','1.3.6.1.2.1.25.2.3.1.5.4'))
    ramUsada = 65536*int(consultaSNMP('eduardoCuevas','172.20.10.7','1.3.6.1.2.1.25.2.3.1.6.4'))

    ramPorcentaje = (ramUsada * 100)/ramTotal
    discoPorcentaje = (discoUsado * 100)/discoTotal
    ramPorcentaje = round(ramPorcentaje,2)
    discoPorcentaje = round(discoPorcentaje,2) 
    
    valor = "N:" + str(avg) + ":" + str(ramPorcentaje) + ":" + str(discoPorcentaje)
    print (valor)
    rrdtool.update(rrdpath+'trend.rrd', valor)
    rrdtool.dump(rrdpath+'trend.rrd',rrdpath+'trend.xml')
    time.sleep(5)

if ret:
    print (rrdtool.error())
    time.sleep(300)
