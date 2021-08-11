import requests
from bs4 import BeautifulSoup
import urlparse

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

def main():
    target_url="http://172.16.212.142/dvwa/login.php"
    response=request(target_url)
    parse_html = BeautifulSoup(response.content)
    forms = parse_html.findAll("form")
    if len(forms)==0:
        print("La pagina no tiene formularios.")
    form_index=1
    input_index=1
    for f in forms:
        print("FORMULARIO "+str(form_index))
        print("--------------------------------------------------------------------------")
        print(f)
        print("--------------------------------------------------------------------------")
        action=f.get("action")
        method=f.get("method")
        print("Action del formulario: "+action)
        print("Metodo del formulario: " + method)
        print("Link completo: "+urlparse.urljoin(target_url,action))
        form_index=form_index+1
        input_list=f.findAll("input")
        data={}
        for i in input_list:
            name=i.get("name")
            type=i.get("type")
            value = i.get("value")
            data[name]=value
            print("Input #"+str(input_index)+" del  name: "+name+", value: "+str(value)+", tipo: "+type)
            input_index=input_index+1
        print("-------------------------------------------------\nDATA PARA REQUEST")
        print(data)

if __name__ == '__main__':
    main()