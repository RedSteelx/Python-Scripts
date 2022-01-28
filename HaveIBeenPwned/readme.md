This script was created in order to check if an email address has been compromised from a data
breach from different websites it was registered on using the API from haveibeenpwned. This
script is written in Python and requires the requests and xlrd library to function. This script
takes email addresses in a list to be written in the code, or an external excel file from column A
and outputs if they are safe or not, the name and date of the leak, and what information was
compromised from those websites. At the beginning of the log file the number of safe email
addresses and breached ones will be displayed. The log is outputted as pwned_log.doc in the
directory the script is run from, so it is necessary to not have a previous pwned_log.doc file in
the folder already or else it will be overwritten.
