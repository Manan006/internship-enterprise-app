from internalapi.cache import cache
from internalapi.methods import methods
import smtplib
import os

defaultMessage="This is the password for your account "
class email:
    def send_password(email,password,message=defaultMessage):
        #reciever is needed all the time,
        #message is optional, and can be used as the default one incase if it's not provided
        try:
            sender= smtplib.SMTP('smtp.gmail.com', 587)
            sender.starttls()
            sender.login(os.getenv('verfiyEmail'),os.getenv('verifyEmailPass'))
            message=message+password
            sender.sendmail(os.getenv('verfiyEmail'), email, message)
            sender.quit()
        except Exception as exception:
            return Response(200,exception)
        return Response(100)
