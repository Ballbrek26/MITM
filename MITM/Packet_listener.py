import scapy.all as scapy
from scapy.layers.http import HTTPRequest

def listen_packets(interface):

    scapy.sniff(iface=interface,store=False,prn=analyze_packets,promisc=True)
    #prn = callback function

def analyze_packets(packet):
    #packet.show()
    if packet.haslayer(HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)

listen_packets("enp0s3")