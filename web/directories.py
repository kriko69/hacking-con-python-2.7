import requests
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", dest="url", help="website")
    (options, arguments) = parser.parse_args()
    if not options.url:
        parser.error("[-] Please specify an url, use --help for more info.")
    return options

def request(url):
    try:
        return requests.get("http://"+url)
    except requests.exceptions.ConnectionError:
        pass

def main():
    options=get_arguments()
    aux=0
    with open('files-and-dirs-wordlist.txt','r') as directory:
        for line in directory:
            word=line.strip()
            test_url=options.url+"/"+word
            response=request(test_url)
            if response:
                aux=aux+1
                print "[+] directorio descubierto --> "+test_url
        print "[+] Fin de la busqueda."
    if aux==0:
        print "[-] No hay directorios descubiertos."
if __name__ == '__main__':
    main()