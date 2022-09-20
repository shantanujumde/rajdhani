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
    receivers = [booking["passenger_email"]]

    message = f"""From: From Person <from@fromdomain.com>
                To: To Person <{receivers[0]}>
                Subject: Your booking is successful

                your booking from  {booking["from_station_name"]} to {booking["to_station_name"]}
                is successfull

                Thankyou!!
                """
    print(config.smtp_hostname)
    try:
        smtpObj = smtplib.SMTP(config.smtp_hostname[0]+":"+config.smtp_port[0])
        smtpObj.sendmail(sender, receivers, message)         
        print ("Successfully sent email")
    except Exception as e:
        print ("Error: unable to send email",e)
    

send_booking_confirmation_email({
        "train_number": "12608",
        "train_name": "Lalbagh Exp",
        "from_station_code": "SBC",
        "from_station_name": "Bangalore",
        "to_station_code": "MAS",
        "to_station_name": "Chennai",
        "ticket_class": "3A",
        "date": "2022-09-22",
        "passenger_name": "Tourist",
        "passenger_email": "shantanu.jumde@travelopia.com",
    })