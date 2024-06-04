import json
import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText


def lambda_handler(event,context):
    
    # firstly make client for s3 bucket
    clientS3 = boto3.client("s3")

    # print(event)
    status=[]
    row = event["data"][0] # gets the first 'row' from event data

    # Define all the needed parts from the request
    # row[0] ... row index
    from_address=row[1] # it's needed for AWS
    to_addresses=row[2]
    cc_addresses=row[3]
    bcc_addresses=row[4]
    subject=row[5]
    body_format=row[6].upper() # needs to be 'Html'
    importance=row[7]
    sensitivity=row[8]
    body=row[9]
    file_attachments=row[10]

    print('Heeeey, oooh')

    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('alternative')

    # Add subject, from and all types of recipients
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = ', '.join(to_addresses)
    msg['Cc'] = ', '.join(cc_addresses)
    msg['Bcc'] = ', '.join(bcc_addresses)
    
    # Add the HTML parts to the child container.
    if body_format == 'TEXT':
        part = MIMEText(body, 'plain')
    elif body_format == 'HTML':
        part = MIMEText(body, 'html')
    msg.attach(part)
 
    print('Listen what I say, oh')

    # Add attachments
    for attachment in file_attachments:
        
        print('I got your "hey, oh"')
        print(attachment)

        s3_file = clientS3.get_object(Bucket='s3-in516ht-ggl-eu-central-1', Key=attachment)
        # print(s3_file)
        print('Now listen what I say, oh (oh)')

        # print(s3_file['Body'].read())

        # with open(s3_file['Body'], 'rb') as f:
        part = MIMEApplication(s3_file['Body'].read())
        part.add_header('Content-Disposition', 'attachemnt', filename=attachment)
        msg.attach(part)

    print('When will I know that I really cant go')
    
    # try:
    # create SES client
    clientSES = boto3.client('ses', region_name='eu-central-1') # add region to the client if needed
    # print(msg.as_string())

    print('To the well once more time to decide on?')

    response = clientSES.send_raw_email(
        Source=from_address,
        Destinations=to_addresses,
        RawMessage={ 'Data': msg.as_string()}
    )

    print('When its killing me, when will I really see')
    print(response)

    status.append([0,'Notification Sent Successfully'])

    print('All that I need to look inside')
    # except:
    #     response = client.verify_email_identity(EmailAddress = from_address)
    #     status.append([0,'Sender Address is not verified , sent mail for verification'])
            
    return {
        'data': status
    }
        
        
