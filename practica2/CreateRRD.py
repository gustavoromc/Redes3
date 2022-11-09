#!/usr/bin/env python
import rrdtool
ret = rrdtool.create("segmentosRed.rrd",
                     "--start",'N',
                     "--step",'300',
                     "DS:paquetesUnicast:COUNTER:120:U:U",
                     "DS:paquetesIPv4:COUNTER:120:U:U",
                     "DS:paquetesICMPecho:COUNTER:120:U:U",
                     "DS:segmentosEntrada:COUNTER:120:U:U",
                     "DS:datagramasSalida:COUNTER:120:U:U",
                     #"DS:segmentosEntrada:COUNTER:120:U:U",
                     #"DS:segmentosSalida:COUNTER:120:U:U",
                     "RRA:AVERAGE:0.5:6:700",
                     "RRA:AVERAGE:0.5:1:1400")

if ret:
    print (rrdtool.error())