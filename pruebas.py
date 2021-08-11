import shutil


def lectura():
    with open('faffy_list','rw') as faffy:
        with open('file_faffy_list','w+') as file_faffy:
            for linea in faffy:
                print linea
                aux = linea.rfind('.')
                nueva_linea = linea[0:aux]
                ex = linea[aux:len(linea)]
                nueva_linea=nueva_linea+'.FAFFY'
                file_faffy.write(nueva_linea+'\n')

    faffy.close()
    file_faffy.close()
def main():
    lectura()

if __name__ == '__main__':
    main()