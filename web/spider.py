import requests
import re
import optparse
import urlparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", dest="url", help="website")
    (options, arguments) = parser.parse_args()
    if not options.url:
        parser.error("[-] Please specify an url, use --help for more info.")
    return options

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass
def crawl(response,url):
    target_links=[]
    href_links = re.findall('(?:href=")(.*?)"', response.content)
    for link in href_links:
        link=urlparse.urljoin(url,link)

        if "#" in link:
            link=link.split("#")[0]

        if url in link and link not in target_links:
            target_links.append(link)
            print link
            crawl(response,link)

def main():
    options=get_arguments()
    response=request(options.url)
    crawl(response,options.url)
if __name__ == '__main__':
    main()
