import socket
from datetime import datetime

date = datetime.now()
date_timee = date.strftime("%m/%d/%Y, %H:%M:%S")
#datetime.strftime(date_string)

hostname = 'x'

addr1 = socket.gethostbyname(x)
print(date,addr1)
#print('\n')
f = open('dns.txt','a')    
f.write(date_timee + ' ')
f.write(addr1 + ' ')
f.write('\n')
f.close()
