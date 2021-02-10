import requests
from datetime import datetime
import smtplib
import time

# Email information
my_email = ""
password = ""

MY_LAT = None # Your latitude
MY_LONG = None # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
print(f"{iss_latitude}, {iss_longitude}")


def is_iss_overhead():
    return (iss_latitude - 5 <= MY_LAT <= iss_latitude + 5) and (iss_longitude - 5 <= MY_LONG <= iss_longitude + 5)


def is_dark():
    hour = int(time_now.strftime("%H:%M:%S")[0:2])
    return sunrise > hour > sunset


while True:
    if is_iss_overhead() and is_dark():
        print("email sending!")
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=my_email,
                                msg="Subject:Look up!\n\nYou can see the ISS now!")
    time.sleep(60)


