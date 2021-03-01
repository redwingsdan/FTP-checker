import yagmail
import ftplib
import schedule
import time
import configparser
from ftplib import FTP_TLS

def send_email():
    global configParser
    USER = configParser.get('email-config', 'username')
    PASS = configParser.get('email-config', 'password')
    TO_EMAILS = [e.strip() for e in configParser.get('email-config', 'to_emails').split(',')]
    SUBJECT = 'FTP File'
    EMAIL_CONTENT = 'There was a file added to the FTP server'
    try:
        #initializing the server connection
        yag = yagmail.SMTP(user=USER, password=PASS)
        #sending the email
        yag.send(to=TO_EMAILS, subject=SUBJECT, contents=EMAIL_CONTENT)
        print("Email sent successfully")
    except all_errors as e:
        print("Error, email was not sent", e)       
        
def check_ftp_for_file(t):
    global configParser
    global prev_file_size
    FTP_SERVER = configParser.get('ftp-config', 'servername')
    USER = configParser.get('ftp-config', 'username')
    PASS = configParser.get('ftp-config', 'password')
    DIR = configParser.get('ftp-config', 'directory')
    FILE_NAME = configParser.get('ftp-config', 'filename')
    ftps = FTP_TLS(FTP_SERVER)
    try:
        ftps.login(USER, PASS)
        ftps.prot_p()  # switch to secure data connection. Otherwise, only the user and password is encrypted and not all the file data.
        ftps.cwd(DIR)
        size = ftps.size(FILE_NAME)
        if prev_file_size != size:
            prev_file_size = size
            send_email()
    except ftplib.all_errors as e:
        prev_file_size = 0
        print('FTP error:', e)
    finally:
        ftps.close()

configParser = configparser.RawConfigParser()   
configFilePath = r'ftpconfig.txt'
configParser.read(configFilePath)
scheduler_minutes = int(configParser.get('ftp-config', 'scheduler_minutes'))
schedule.every(scheduler_minutes).minutes.do(check_ftp_for_file, 'Checking FTP')       
prev_file_size = 0 
while True:
    schedule.run_pending()
    print('Waiting to check ftp')
    time.sleep(scheduler_minutes * 60) # wait one minute
#check_ftp_for_file(None)