import requests
import time
import sys
import xlrd

#Insert list of emails here for manual
emails = []

rate = 1.5

#/Users/gmanikanden/Desktop/scripts/emails.xlsx
location = input("Location of excel sheets containing email (n if none): " )

if location != 'n':
         
         wb = xlrd.open_workbook(location)
         sheet = wb.sheet_by_index(0)
         sheet.cell_value(0,0)

         for i in range(sheet.nrows):
                  if ('@' in sheet.cell_value(i,0)):
                           emails.append(sheet.cell_value(i,0))
      


#name of breach, date, description

def main():
         global safe, breached
         original = sys.stdout
         sys.stdout = open('pwned_log.doc','w')

         safe = 0
         breached = 0
         for x in emails:
                  checkEmail(x)
        
         sys.stdout = original

         totalx = 'Safe Email Addresses: ' + str(safe) + '    '
         totaly = 'Breached Email Addresses: ' + str(breached)
         
         with open('/Users/gmanikanden/Desktop/scripts/pwned_log.doc', 'r+') as file:
                  content = file.read()
                  file.seek(0,0)
                  file.write(totalx + totaly + '\n\n' + content)
                  
def checkEmail(email):
         uri = 'https://haveibeenpwned.com/api/v2/breachedaccount/' + email
         headers = {'User-Agent': 'Gajesh Pwnage Checker'}
         response = requests.get(uri,headers=headers, verify=True)
         i = 0
        
         print('Email: ' + email)
         
         if str(response.status_code) == '404':
                  print('Safe')
                  global safe
                  safe = safe + 1
                  time.sleep(rate)
                  
         elif str(response.status_code) == '200':
                  data = response.json()
                  global breached
                  breached = breached + 1
                  try:
                           while (True):
                                    
                                    print(data[i]['Name'], end ='    ')
                                    
                                    
                                    print(data[i]['BreachDate'], end = '    ')
                                    print('[%s]' % ', '.join(map(str,data[i]['DataClasses'])), end ='    ')
                                   
                                     
                                    print()
                                    
                                    i = i+1
                  except:
                           pass
                  
                  time.sleep(rate)
         elif str(response.status_code) == '429':
                  time.sleep(int(response.headers['Retry-After']))
                  checkEmail(email)
         else:
                  print('Yikes what happened', end ='    ')
                  time.sleep(rate)
         print()



if __name__ == "__main__":
    main()
