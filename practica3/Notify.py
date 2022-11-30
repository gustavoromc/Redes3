from email.mime.text import MIMEText
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from getSNMP import consultaSNMP

COMMASPACE = ', '
# Define params
rrdpath = './rrd/'
imgpath = './img/'
fname = 'trend.rrd'

mailsender = "gustavoromguest@gmail.com"
#mailreceip = "dummycuenta3@gmail.com"
mailreceip = "gustavoromguest@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'zsuvabkmpwjfgvds'

def send_alert_attached(subject, content, imagen):

    datosSNMP = consultaSNMP("eduardoCuevas", "172.20.10.7", "1.3.6.1.2.1.1.1.0")
    os = "hola"
    if datosSNMP.find("Linux") == 1:
        os = "Linux"
    else:
        os = "Windows"
    
    name = consultaSNMP("eduardoCuevas", "172.20.10.7", "1.3.6.1.2.1.1.5.0")
    contact = consultaSNMP("eduardoCuevas", "172.20.10.7", "1.3.6.1.2.1.1.4.0")
    ubi = consultaSNMP("eduardoCuevas", "172.20.10.7", "1.3.6.1.2.1.1.6.0")

    content = content + "\nDispositivo: " + name + "\nSistema Operativo: " + os + "\nContacto: " + contact + "\nUbicacion: " + ubi

    """ Envía un correo electrónico adjuntando la imagen en IMG
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(imagen, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(MIMEText(content, 'plain'))
    msg.attach(img)
    
    s = smtplib.SMTP(mailserver)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, mailreceip, msg.as_string())
    s.quit()

send_alert_attached("Hola", "Hola", "./img/RAM.png")