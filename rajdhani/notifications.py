"""Email notifications on bookings.
"""
from . import config
import smtplib
from email.message import EmailMessage

def send_booking_confirmation_email(booking):
    """Sends a confirmation email on successful booking.
    The argument `booking` is a row in the database that contains the following fields:
        id, name, email, train_number, train_name, ticket_class, date
    """
    # The smtp configuration is available in the config module
    email = EmailMessage()
    email['Subject'] = 'Your Booking Successful!'
    email['From'] = 'Shantanu Jumde <shantanujumde@rajdhani.pipal.in>'
    email['To'] = f'{booking["passenger_name"]} <{booking["passenger_email"]}>'
    email.set_content(f"""Dear Passanger,
    Your booking from  {booking["from_station_name"]} to {booking["to_station_name"]}
    is successfull

    Team Rajdhani
    """)
    print(config.smtp_hostname)
    smtpObj = smtplib.SMTP(f'{config.smtp_hostname[0]}:{config.smtp_port[0]}')
    try:
        if config.smtp_username[0]:
            smtpObj.starttls()
            smtpObj.login(config.smtp_username[0], config.smtp_password[0])
        smtpObj.send_message(email)
        print("Email Send Success")
    except Exception as e:
        print ("Error: unable to send email",e)
    finally:
        smtpObj.quit()
    

# send_booking_confirmation_email({
#         "train_number": "12608",
#         "train_name": "Lalbagh Exp",
#         "from_station_code": "SBC",
#         "from_station_name": "Bangalore",
#         "to_station_code": "MAS",
#         "to_station_name": "Chennai",
#         "ticket_class": "3A",
#         "date": "2022-09-22",
#         "passenger_name": "Tourist",
#         "passenger_email": "shantanu.jumde@travelopia.com",
#     })