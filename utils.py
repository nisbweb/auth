import smtplib
import os
from random import randint

def generate_token(digits):
    range_start = 10**(digits-1)
    range_end = (10**digits)-1
    return str(randint(range_start, range_end))

def send_email_with_token(email, token):
    server = smtplib.SMTP_SSL('smtp.yandex.com:465')
    server.ehlo()
    server.login(os.environ["EMAIL_USERNAME"],os.environ["EMAIL_PASSWORD"])
    message = 'Subject: NISB Password Reset\n\n' + \
            'An attempt was made to reset the password.\n' + \
            'Please use the following as token for the same\n' + token + \
            '\nIf you did not try to reset the password, you don\'t need to do anything.'
    server.sendmail(os.environ["EMAIL_USERNAME"],email,message)
    server.quit()
    return True


# if __name__ == "__main__":
#     token = (generate_token(6))
#     send_email_with_token("mridul.kepler@gmail.com",token)