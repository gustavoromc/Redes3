import time
import rrdtool
from getSNMP import consultaSNMP
while 1:
    pack_uni = int (
        consultaSNMP('eduardoCuevas','192.168.1.77',
                     '1.3.6.1.2.1.2.2.1.11.3'))
    pack_ipv4 = int (
        consultaSNMP('eduardoCuevas','192.168.1.77',
                     '1.3.6.1.2.1.4.3.0'))
    msjs_ICMP = int (
        consultaSNMP('eduardoCuevas','192.168.1.77',
                     '1.3.6.1.2.1.5.8.0'))
    segmentos_entrada = int (
        consultaSNMP('eduardoCuevas','192.168.1.77',
                     '1.3.6.1.2.1.6.10.0'))
    datagramas_UDP = int (
        consultaSNMP('eduardoCuevas','192.168.1.77',
                     '1.3.6.1.2.1.7.1.0'))


    # tcp_in_segments = int(
    #     consultaSNMP('eduardoCuevas','192.168.1.77',
    #                  '1.3.6.1.2.1.6.10.0'))
    # tcp_out_segments = int(
    #     consultaSNMP('eduardoCuevas','192.168.1.77',
    #                  '1.3.6.1.2.1.6.11.0'))
    valor = "N:" + str(pack_uni) + ':' + str(pack_ipv4) + ':' + str(msjs_ICMP) + ':' + str(segmentos_entrada) + ':' + str(datagramas_UDP)
    print (valor)
    rrdtool.update('segmentosRed.rrd', valor)
    rrdtool.dump('segmentosRed.rrd','traficoRED.xml')
    time.sleep(1)

if ret:
    print (rrdtool.error())
    time.sleep(300)