import requests
#import smtplib
import json
import sys

key = ''
email = []
name = []


#y = is to get users


def get_users_not_clicked():
    
    counter = 1
    counter_2 = 0
    
    while counter != 10:
        print(counter)
        y = requests.get('https://us.api.knowbe4.com/v1/phishing/xxx', headers={'Content-Type':'application/json',
                       'Authorization': 'Bearer {}'.format(key)}, params = {'page': counter, 'per_page': 500})
        
        y = y.json()
        #print(y)
        if (y == []):
            break
        for x in y:
            if ( x['clicked_at'] != None): #change this for who clicked from != to ==
               
                name_append = x['user']['first_name']
                #print(name_append)
                email_append = x['user']['email']
                #print(email_append)
                #########################
                name.append(name_append)
                email.append(email_append)

        counter = counter + 1
        
    
    print(len(email))   
    sys.stdout = open('email_list.txt','w')
    for acc in email:
        print(acc, sep='', end=';', flush=True)
        sys.stdout.flush()
        
        counter_2 = counter_2 + 1
        if (counter_2 % 500 == 0):
            print('xyz', sep='', end=';', flush=True)
            sys.stdout.flush()
        
    sys.stdout.close()
def send_email():
    get_users_not_clicked()
    sender = 'xxxxx@gmail.com'
    counter = 0
    
    while counter < len(email):
        
        receiver = email[counter]
        n = name[counter]
        counter = counter + 1



        message ="""From: xxx xxx <xxx@xxx.com>
        To: User <"""+ receiver + """>
        Subject: xxx Test

        Hello """ + n + """,

        Test.

        Regards,

        xxx xxx
        Vice President and CISO
        xxx xxx xxx Inc.
        xxx xxx xxx xxx, x xxx | xxx, x xxx
        o: x-x-x
        x@x.com  |  www.x.com
 

        """
        #print(message)

        #s = smtplib.SMTP(host='smtp.x.com', port=25)
        #s.starttls()
        #s.sendmail(sender,receiver,message)


get_users_not_clicked()


