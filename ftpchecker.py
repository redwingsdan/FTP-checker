import yagmail
import ftplib
import schedule
import time
from ftplib import FTP_TLS

def send_email():
    USER = 'gmailacct@gmail.com'
    PASS = 'gmailacctpassword'
    TO_EMAILS = ['toaddress@address.com', 'othertoaddress@secondaddress.com']
    SUBJECT = 'Email Subject'
    EMAIL_CONTENT = 'This is the content of the email'
    try:
        #initializing the server connection
        yag = yagmail.SMTP(user=USER, password=PASS)
        #sending the email
        yag.send(to=TO_EMAILS, subject=SUBJECT, contents=EMAIL_CONTENT)
        print("Email sent successfully")
    except:
        print("Error, email was not sent")       
        
def check_ftp_for_file(t):
    FTP_SERVER = 'ftp.pureftpd.org'
    USER = 'ftp user'
    PASS = 'ftp pass'
    DIR = 'file/dir/path'
    FILE_NAME = 'file.txt'
    ftps = FTP_TLS(FTP_SERVER)
    try:
        ftps.login(USER, PASS)
        ftps.prot_p()  # switch to secure data connection. Otherwise, only the user and password is encrypted, this way file data is also encrypted
        ftps.cwd(DIR)
        size = ftps.size(FILE_NAME)
        send_email()
    except ftplib.all_errors as e:
        print('FTP error:', e)
    finally:
        ftps.close()

schedule.every().minute.do(check_ftp_for_file, 'Checking FTP')        
while True:
    schedule.run_pending()
    print('Waiting to check ftp')
    time.sleep(60) # wait one minute
#check_ftp_for_file(None)
