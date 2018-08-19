import socket

hosts = ["8.8.8.8"]

ports = [21,22, 23, 25, 80, 110, 443, 445, 3389,8080]

for host in hosts:
    for port in ports:
        try:
            print ("Connecting to " + host + ":" + str(port))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            result = s.connect_ex((host, port))
            if result == 0:
                print ("Port " + str(port) + " open!")
                print (str(s.recv(1024)))
                
            s.close()
        except:
            print("Timeout")
            pass
