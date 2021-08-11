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
    with open('subdomains-wodlist.txt','r') as subdomains:
        for line in subdomains:
            word=line.strip()
            test_url=word+"."+options.url
            response=request(test_url)
            if response:
                aux=aux+1
                print "[+] Subdominio descubierto --> "+test_url
        print "[+] Fin de la busqueda."
    if aux==0:
        print "[-] No hay dominios descubiertos."
if __name__ == '__main__':
    main()