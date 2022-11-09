from datetime import datetime
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table,)
from pysnmp.hlapi import *
from reportlab.pdfgen import canvas
import time
import rrdtool

def consultaSNMP(comunidad,host,oid, puerto):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, int(puerto))),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split("=")[1]
    return resultado

def agregarDispositivo():
    print()
    comunidad = input("Comunidad: ")
    version = input("Version: ")
    puerto = input("Puerto: ")
    ip = input("IP: ")

    with open("bdd.txt", "a") as file:
        file.write(comunidad + " " + version + " " + puerto + " " + ip + "\n")

def change():
    print()
    i = 1
    print("Dispositivos: ")
    with open("bdd.txt", "r") as file:
        datos = file.readlines()

    with open("bdd.txt", "r") as file:
        for line in file:
            print(str(i) + "\t" + line)
            i = i + 1

    borrar = int(input("Dispositivo a modificar: "))
    i = 1
    print()
    comunidad = input("Comunidad: ")
    version = input("Version: ")
    puerto = input("Puerto: ")
    ip = input("IP: ")
    print()

    with open("bdd.txt", "w") as file:
        for line in datos:
            if i != borrar:
                file.write(line)
            else:
                file.write(comunidad + " " + version + " " + puerto + " " + ip + "\n")
            i = i + 1

def delete():
    print()
    i = 1
    
    with open("bdd.txt", "r") as file:
        datos = file.readlines()
    print("Dispositivos: ")
    with open("bdd.txt", "r") as file:
        for line in file:
            print(str(i) + "\t" + line)
            i = i + 1
    
    borrar = int(input("Dispositivo a borrar: "))
    i = 1
    with open("bdd.txt", "w") as file:
        for line in datos:
            if i != borrar:
                file.write(line)
            i = i + 1

def report():
    print()
    
    with open("bdd.txt", "r") as file:
        devices = file.readlines()

    i = 1
    print("Dispositivos: ")
    with open("bdd.txt", "r") as file:
        for line in file:
            print(str(i) + "\t" + line)
            i = i + 1
    # numero = int(input("Dispositivo a generar reporte: ")) - 1
    numero = 0
    datos = devices[numero].split()

    comunidad = datos[0]
    version = datos[1]
    puerto = datos[2]
    ip = datos[3]

    datosSNMP = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.1.0", puerto)
    os = "hola"
    if datosSNMP.find("Linux") == 1:
        os = datosSNMP.split()[0]
    else:
        os = datosSNMP.split()[12]
    
    name = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.5.0", puerto)
    contact = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.4.0", puerto)
    ubi = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.6.0", puerto)
    numInter = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.1.0", puerto)

    """ print(os)
    print(name)
    print(contact)
    print(ubi)
    print(numInter) """

    i = 1
    interfaces = []
    while i <= 6:
        interfaz = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.7." + str(i), puerto)
        interfaces.append(interfaz)
        # print(str(i))
        i = i + 1
    #print(interfaces)

    timestr = time.strftime("%Y%m%d-%H%M%S")

    output = canvas.Canvas("SNMPreport" + timestr + ".pdf")
    output.setTitle("SNMPReport")
    output.drawString(50, 800, "Administración de Servicios en Red")
    output.drawString(50, 775, "Práctica 2")
    output.drawString(50, 750, "Victor Gustavo Romero Cisneros 4CM13")

    output.drawString(75, 700, "Nombre del dispositivo: " + name)
    output.drawString(75, 725, "S.O.: " + os)
    output.drawString(75, 675, "Info. de contacto: " + contact)
    output.drawString(75, 650, "Ubicacion: " + ubi)
    output.drawString(75, 625, "# de interfaces: " + numInter)
    """ while i <= 6:
        if os.find("Linux") == 0:
            res = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.2." + str(i), puerto)
            output.drawString(75, pixels, res + " " + interfaces[i - 1])
        else: 
            res = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.2." + str(i), puerto)[3:]
            output.drawString(75, pixels, bytes.fromhex(res).decode('utf-8') + " " + interfaces[i - 1])
        i = i + 1
        pixels = pixels - 25 """

    i = 1
    if int(numInter) > 6 :
        max = 6
    else: 
        max = int(numInter)
    matriz = [["INTERFACE", "STATUS"]]
    while i <= max:
        if os.find("Linux") != -1:
            descrInterfaz = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.2." + str(i), puerto)
        else:
            res = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.2." + str(i), puerto)[3:]
            descrInterfaz = bytes.fromhex(res).decode('utf-8')

        estadoInterfaz = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.7." + str(i), puerto)

        if estadoInterfaz == " 1":
            matriz.append([descrInterfaz, "UP"])
        elif estadoInterfaz == " 2":
            matriz.append([descrInterfaz, "DOWN"])
        else:
            matriz.append([descrInterfaz, "TESTING"])
        i = i + 1

    width = 200
    height = 400
    x = 50
    y = 450
    f = Table(matriz)
    f.wrapOn(output, width, height)
    f.drawOn(output, x, y)
    


    output.showPage()

    output.drawString(50, 800, "Administración de Servicios en Red")
    output.drawString(50, 775, "Práctica 2")
    output.drawString(50, 750, "Victor Gustavo Romero Cisneros 4CM13")
    output.drawString(50, 725, "version: 1")
    output.drawString(50, 700, "device: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.5.0", puerto))
    output.drawString(50, 675, "date: " + time.strftime("%d/%m/%Y - %H:%M:%S"))
    output.drawString(50, 650, "dafaultProtocol: radius")
    output.drawString(50, 625, "rdate: " + time.strftime("%d/%m/%Y - %H:%M:%S"))
    output.drawString(50, 600, "")
    output.drawString(50, 575, "#User-Name")
    output.drawString(50, 550, "1: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.4.0", puerto))
    output.drawString(50, 525, "#Acct-Input-Octets")
    output.drawString(50, 500, "42: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.10.3", puerto))
    output.drawString(50, 475, "#Acct-Output-Octets")
    output.drawString(50, 450, "43: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.16.3", puerto))
    output.drawString(50, 425, "#Acct-Session-Time")
    output.drawString(50, 400, "46: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.3.0", puerto))
    output.drawString(50, 375, "#Acct-Input-Packets")
    output.drawString(50, 350, "47: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.11.3", puerto))
    output.drawString(50, 325, "#Acct-Output-Packets")
    output.drawString(50, 300, "48: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.17.3", puerto))

    output.showPage()

    output.drawString(50, 800, "Administración de Servicios en Red")
    output.drawString(50, 775, "Práctica 2")
    output.drawString(50, 750, "Victor Gustavo Romero Cisneros 4CM13")
    output.drawInlineImage( "./pack_uni.png", 50, 600, 200, 125)
    output.drawInlineImage( "./pack_ipv4.png", 300, 600, 200, 125)
    output.drawInlineImage( "./msjs_ICMP.png", 50, 450, 200, 125)
    output.drawInlineImage( "./segmentos_entrada.png", 300, 450, 200, 125)
    output.drawInlineImage( "./datagramas_UDP.png", 50, 300, 200, 125)
    
    output.showPage()

    output.save()

    """ i = 1
    with open("bdd.txt", "r") as file:
        for line in file:
            print(str(i) + "\t" + line)
            i = i + 1 """
            
def graph():

    print("Escriba la fecha inicial (Y/m/d H:M:S):")
    fechaInicial = input()
    print("Escriba la fecha final (Y/m/d H:M:S):")
    fechaFinal = input()

    tiempo_final =  int(datetime.strptime(fechaFinal, "%Y/%m/%d %H:%M:%S").timestamp())
    tiempo_inicial = int(datetime.strptime(fechaInicial, "%Y/%m/%d %H:%M:%S").timestamp())

    ret = rrdtool.graphv("pack_uni.png",
                        "--start", str(tiempo_inicial),
                        "--end", str(tiempo_final),
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
                        "--end", str(tiempo_final),
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
                        "--end", str(tiempo_final),
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
                        "--end", str(tiempo_final),
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
                        "--end", str(tiempo_final),
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
    #print(ret)


print("#################################################")
print("\tAdmin. Serv. en Red")
print("\t4CM13")
print("\tPractica 2 - Sistema de Contabilidad")
print("\tRomero Cisneros Victor Gustavo")
print("#################################################")

graph()
report()