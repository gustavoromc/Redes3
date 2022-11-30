import rrdtool
ret = rrdtool.create("rrd/trend.rrd",
                     "--start",'N',
                     "--step",'30',
                     "DS:CPUload:GAUGE:60:0:100",
                     "DS:RAMload:GAUGE:60:0:100",
                     "DS:DISKload:GAUGE:60:0:100",
                     "RRA:AVERAGE:0.5:1:1000")
if ret:
    print (rrdtool.error())
