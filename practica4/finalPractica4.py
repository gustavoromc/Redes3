import telnetlib
from ftplib import FTP
import subprocess

user = "rcp"
pas = "rcp"

def generarArchivo():
	print("\n---Ingrese la direccion IP del router:")
	host = input()
	tn = telnetlib.Telnet()
	tn.open(host)
	tn.read_until(b"User: ")
	tn.write(user.encode("ascii")+b"\r\n")
	tn.read_until(b"Password: ")
	tn.write(pas.encode("ascii")+b"\r\n")
	tn.write(b"en\r\n")
	tn.write(b"config\r\n")
	tn.write(b"copy run start\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.read_all()
	tn.close()
	print("\n------startup-config CREADO------\n")
	menu()
def extraerArchivo():
	print("\n---Ingrese la direccion IP del router:")
	host = input()
	print("\n\t------Proporcione un nombre para el router:")
	name = input()
	tn = telnetlib.Telnet()
	tn.open(host)
	tn.read_until(b"User: ")
	tn.write(user.encode("ascii")+b"\r\n")
	tn.read_until(b"Password: ")
	tn.write(pas.encode("ascii")+b"\r\n")
	tn.write(b"en\r\n")
	tn.write(b"config\r\n")
	tn.write(b"service ftp\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.read_all()
	tn.close()
	
	ftp = FTP (host)
	ftp.login(user,pas)
	ftp.retrbinary('RETR startup-config',open('startup-config-' + name , 'wb').write)
	ftp.quit()
	print("------startup-config DESCARGADO------")
	menu()
def importarArchivo():
	print("\n---Ingrese la direccion IP del router:")
	host = input()
	print("\n\t------Proporcione un nombre para el router:")
	name = input()
	tn = telnetlib.Telnet()
	tn.open(host)
	tn.read_until(b"User: ")
	tn.write(user.encode("ascii")+b"\r\n")
	tn.read_until(b"Password: ")
	tn.write(pas.encode("ascii")+b"\r\n")
	tn.write(b"en\r\n")
	tn.write(b"config\r\n")
	tn.write(b"service ftp\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.read_all()
	tn.close()
	
	ftp = FTP (host)
	ftp.login(user,pas)
	f = open('startup-config-'+name,'rb')
	ftp.storbinary('STOR startup-config',f)
	f.close()
	ftp.quit()
	print("-----startup-config ENVIADO------")
	menu()
	
def menu():
	print("++++++PRACTICA 4+++++")
	print("Administracion de servicios en Red")
	print("\n\nIngrese una opcion:")
	print("1. Generar archivo de configuración...")
	print("2. Extraer archivo de configuración...")
	print("3. Importar archivo de configuración...")
	opc = input()
	if opc =="1":
		generarArchivo()
	if opc == "2":
		extraerArchivo()
	if opc == "3":
		importarArchivo()
	
	if opc > "3" or opc < "1":
		exit()
	

menu()
