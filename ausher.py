import smtplib
import requests
from datetime import datetime
import random


SB_ENDPOINT = "https://sheet.best/api/sheets/c0889e23-b519-4214-b4b3-aa455777a646"
MY_EMAIL = "MAIL ID"
MY_PASSWORD = "MAIL PASSWORD"

today = datetime.now()
today_tuple = (today.month, today.day)

response = requests.get(url=SB_ENDPOINT)
# print(response.raise_for_status)
data = response.json()
birthday_dict = {}

for i in data:
    name = i["Name"]
    email = i["Email"]
    month = i["Date of Birth"].split("/")[0]
    day = i["Date of Birth"].split("/")[1]
    birthday_dict[(int(month),int(day))] = [name,email]

if today_tuple in birthday_dict:
    birthday_person = birthday_dict[today_tuple][0]
    birthday_email = birthday_dict[today_tuple][1]
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person)

    with smtplib.SMTP("smtp.google.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_email,
            msg=f"Subject:Happy Birthday!\n\n{contents}"
        )
    
