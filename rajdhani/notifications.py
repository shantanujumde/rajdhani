"""Email notifications on bookings.
"""
from . import config
import smtplib
def send_booking_confirmation_email(booking):
    """Sends a confirmation email on successful booking.
    The argument `booking` is a row in the database that contains the following fields:
        id, name, email, train_number, train_name, ticket_class, date
    """
    # The smtp configuration is available in the config module
    print(booking)
    sender = 'from@fromdomain.com'
    receivers = ['to@todomain.com']

    message = """From: From Person <from@fromdomain.com>
                To: To Person <to@todomain.com>
                Subject: SMTP e-mail test

                This is a test e-mail message.
                """
    try:
        smtpObj = smtplib.SMTP(config.smtp_hostname+":"+config.smtp_port)
        smtpObj.sendmail(sender, receivers, message)         
        print ("Successfully sent email")
    except Exception as e:
        print ("Error: unable to send email")
    
