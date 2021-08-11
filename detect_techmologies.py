import builtwith
import optparse

def get_argument():
    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", dest="url", help="Website")
    (options, arguments) = parser.parse_args()
    if not options.url:
        parser.error("[-] Please specify an url, use --help for more info.")
    return options

def detect(url):
    website=builtwith.parse(url)
    for key,value in website.iteritems():
        print key+":",value

def main():
    options=get_argument()
    detect(options.url)

if __name__ == '__main__':
    main()
