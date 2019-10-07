import yagmail
import os
from random import randint

def generate_token(digits):
    range_start = 10**(digits-1)
    range_end = (10**digits)-1
    return str(randint(range_start, range_end))

def send_email_with_token(email, token):
    yag = yagmail.SMTP(os.environ["EMAIL_USERNAME"], os.environ["EMAIL_PASSWORD"])
    print(os.environ["EMAIL_USERNAME"], os.environ["EMAIL_PASSWORD"])
    contents = ['An attempt was made to reset the password.',
            'Please use the following as token for the same', token, 
            ' If you did not try to reset the password, you don\'t need to do anything.']
    yag.send(email, 'NISB Password Reset', contents)



# if __name__ == "__main__":
#     print(generate_token(6))