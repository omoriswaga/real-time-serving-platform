import json
import logging
import urllib3
from webhooks import webhooks, email_address
import sys
import ast
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(stream=sys.stdout, format=Log_Format, level=logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

http = urllib3.PoolManager()

def flatten_json(d):
    if len(d) == 0:
        return {}
    from collections import deque
    q = deque()
    res = dict()
    for key, val in d.items():  # This loop push the top most keys and values into queue.
        if not isinstance(val, dict):  # If it's not dict
            if isinstance(val, list):  # If it's list then check list values if it contains dict object.
                temp = list()  # Creating temp list for storing the values that we will need which are not dict.
                for v in val:
                    if not isinstance(v, dict):
                        temp.append(v)
                    else:
                        q.append(
                            (key, v))  # if it's value is dict type then we push along with parent which is key.
                if len(temp) > 0:
                    res[key] = temp
            else:
                res[key] = val
        else:
            q.append((key, val))
    while q:
        k, v = q.popleft()  # Taking parent and the value out of queue
        for key, val in v.items():
            new_parent = k + "_" + key  # New parent will be old parent_currentval
            if isinstance(val, list):
                temp = list()
                for v in val:
                    if not isinstance(v, dict):
                        temp.append(v)
                    else:
                        q.append((new_parent, v))
                if len(temp) >= 0:
                    res[new_parent] = temp
            elif not isinstance(val, dict):
                res[new_parent] = val
            else:
                q.append((new_parent, val))
    return res

def format_email(message, message_type):
    formatted_message = ''
    if message_type == 'json':
        msg = ast.literal_eval(message)
        flattened_message = flatten_json(msg)

        for i in flattened_message:
            formatted_message += str(i) + ': ' + str(flattened_message[i]) + '\n'
    else:
        formatted_message = message

    return formatted_message

def send_to_teams(team, subject,  message, alert_type, teams_url, message_type='text'):

    print(message)
    if message_type == 'json':

        message = ast.literal_eval(message)

        msg = flatten_json(message)
        msg.pop('team', None)
        facts = [{"name": key, "value": json.dumps(msg[key])} for key in msg.keys()]
    else:
        facts = [{"name": 'Message', "value": message}]

    facts.append({"name": 'Team', "value": team})

    for url in teams_url:

        body = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": "Kafka Platform Monitoring",
            "themeColor": "0078D7",
            "sections": [
                {
                    "activityTitle": "Kafka Notification",
                    "startGroup": True,

                },
                {
                    "activityTitle": subject,
                    "startGroup": True,
                    "facts": facts

                }
            ],
        }
        activityImage = None
        if alert_type == 'Info':
            activityImage = "https://icon-library.com/images/info-xxl_81067.png"
        elif alert_type == 'Error':
            activityImage = "https://icon-library.com/images/attention-icon/attention-icon-10.jpg"

        if activityImage:
            body['sections'][1]['activityImage'] = activityImage


        resp = http.request('POST', url, body=json.dumps(body).encode('utf-8'))
        response = {
            "message": message,
            "status_code": resp.status,
            "response": resp.data
        }

    return response

def send_email(subject, err_message, teams, sender_email, sender_password=None, message_type='string'):

    if message_type == 'json':
        formatted_message = format_email(message, message_type)
    else:
        formatted_message=err_message
    address_list = []
    if teams:
        for team in teams:
            address_list.append(email_address.get(team))
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(address_list)
    message["Subject"] = subject

    # Attach the body of the email
    message.attach(MIMEText(formatted_message, "plain"))

    # with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    with smtplib.SMTP("server", 1025) as server:
        server.ehlo()
        # server.starttls() #this is commented out because I am using a local smtp server {python3 -m smtpd -c DebuggingServer -n localhost:1025} to begin
        # server.login(sender_email, sender_password)
        server.sendmail(sender_email, address_list, message.as_string())
        server.close()
