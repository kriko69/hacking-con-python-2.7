# coding=utf-8

# my original MAC for wlo1 is e0:94:67:71:ef:c1
import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Interface to change MAC address")
    parser.add_option("-m","--mac",dest="new_mac",help="New MAC address for the interface")
    (options,arguments)=parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    if not options.new_mac:
        parser.error("[-] Please specify a new MAC address, use --help for more info.")
    return options

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    actual_mac_address = re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if actual_mac_address:
        #print(actual_mac_address.group(0))  # group(0) es la primera ocurrencia de un iterable de casos coincidentes
        return actual_mac_address.group(0)
    else:
        print("[-] Could not read the MAC address.")

def change_mac(interface,new_mac):
    print("[+] Changing MAC address for "+interface+" to "+new_mac)
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac]) #se ejecuta comando con call() y se pasa palabra por palabra
    subprocess.call(["ifconfig",interface,"up"])




def main():
    options=get_arguments();
    change_mac(options.interface, options.new_mac)
    #verify changed MAC address
    actual_mac=get_current_mac(options.interface)
    #print("[+] Currently MAC address for interface "+options.interface+": "+str(actual_mac))
    if actual_mac==options.new_mac:
        print("[+] MAC address was successfully changed to "+actual_mac)
    else:
        print("[-] MAC address did not get changed.")

if __name__ == '__main__':
    main()

#example
#sudo python mac_changer.py -i wlo1 -m 1a:2b:3c:4d:5e:6f
