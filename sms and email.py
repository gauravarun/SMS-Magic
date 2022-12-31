import csv
import datetime
import smtplib
import re
import pytz
import requests

# Function to send a text message
def send_text_message(phone_number, message):
    url = "https://api.sms-magic.com/v1/sms/send/bulk"
    sms_text = message
    mobile_number = phone_number

    payload = f"{sms_text,mobile_number}"
    headers = {
        'apikey': "9f81fddf27be1aa3e73a0619392cbc0c",
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response)

# Function to send an email
def send_email(to, subject, message):
    # Set up the SMTP server
    server = smtplib.SMTP('smtp-relay.sendinblue.com')
    # Login to the SMTP server
    server.login('arun.gaurav22@gmail.com', 'JRPpS1OwCn9Ehzyx')
    # Send the email
    server.sendmail('sender@example.com', to, f'Subject: {subject}\n\n{message}')
    # Disconnect from the SMTP server
    server.quit()

# Function to check if a phone number is valid
def is_valid_phone_number(phone_number):
    if isinstance(phone_number, int) and len(str(phone_number)) == 10:
        return True
    return False

# Function to check if an email address is valid
def is_valid_email_address(email_id):
    if re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
        return True
    return False

# Function to check if it is within the specified time range to send a text message
def is_within_text_message_time_range(country):
    # Get the current time in the specified timezone
    current_time = datetime.datetime.now(pytz.timezone(country))
    # Check if the current time is within the specified time range
    if current_time.hour >= 10 and current_time.hour <= 17:
        return True
    return False

# Open the CSV file
with open('sample.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Skip the header row
    next(csv_reader)
    # Iterate over the rows in the CSV file
    for row in csv_reader:
        message = row[0]
        email_id = row[1]
        phone_number = row[2]
        country = row[3]
        schedule_on = row[4]

        # Check if the message should be sent immediately or on a future date
        if schedule_on:
            # Parse the scheduled date
            scheduled_date = datetime.datetime.strptime(schedule_on, '%d-%m-%Y')
            # Check if the scheduled date has passed
            if scheduled_date < datetime.datetime.now():
                # The scheduled date has passed, so don't send the message
                with open('write.txt', 'a') as output_file:
                    output_file.write(f'Failed to send message "{message}" to {email_id} or {phone_number} because the scheduled date has passed\n')
                continue
        else:
            # The message should be sent immediately
            scheduled_date = None

        # Check if the message has a valid length
        if len(message) > 1 and len(message) <= 160:
            # Check if the phone number is valid
            if is_valid_phone_number(phone_number):
                # Check if it is within the specified time range to send a text message
                if is_within_text_message_time_range(country):
                    # Send the text message
                    send_text_message(phone_number, message)
                else:
                    # It is not within the specified time range to send a text message, so don't send it
                    with open('write.txt', 'a') as output_file:
                        output_file.write(
                            f'Failed to send message "{message}" as a text message to {phone_number} because it is not within the specified time range\n')
            else:
                    # The phone number is not valid, so don't send a text message
                    with open('write.txt', 'a') as output_file:
                        output_file.write(
                             f'Failed to send message "{message}" as a text message to {phone_number} because the phone number is not valid\n')
        else:
                # The message is not long enough to be sent as a text message, so don't send it
                with open('write.txt', 'a') as output_file:
                    output_file.write(
                        f'Failed to send message "{message}" as a text message because it is not long enough\n')

        if is_valid_email_address(email_id):
            send_email('recipient@example.com', 'Hello', 'Hello, how are you today?')
        else:
            # The email address is not valid, so don't send the email
            with open('write.txt', 'a') as output_file:
                output_file.write(
                    f'Failed to send message "{message}" as an email to {email_id} because the email address is not valid\n')
