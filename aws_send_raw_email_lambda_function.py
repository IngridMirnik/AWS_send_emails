import io
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
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
    msg = MIMEMultipart('mixed')

    # Add subject, from and all types of recipients
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = ', '.join(to_addresses)
    msg['CC'] = ', '.join(cc_addresses)
    msg['BCC'] = ', '.join(bcc_addresses)
    
    msg_body = MIMEMultipart('alternative')
    # Add the HTML parts to the child container.
    if body_format == 'TEXT':
        part = MIMEText(body.encode('utf-8'), 'plain', 'utf-8')
    elif body_format == 'HTML':
        part = MIMEText(body.encode('utf-8'), 'html', 'utf-8')
    
    msg_body.attach(part)
    msg.attach(msg_body)
    print('Listen what I say, oh')

    # Add attachments
    for attachment in file_attachments:
        
        print('I got your "hey, oh"')
        print(attachment)

        # get the file from s3 bucket
        s3_file = clientS3.get_object(Bucket='s3-in516ht-ggl-eu-central-1', Key=attachment)
        # print(s3_file)
        print('Now listen what I say, oh (oh)')

        # Convert attachment to MIME type
        part2 = MIMEApplication(s3_file['Body'].read())
        part2.add_header('Content-Disposition', 'attachemnt', filename=attachment)

        msg.attach(part2)

    print('When will I know that I really cant go')
    # print(msg.as_string())
    
    # create SES client
    clientSES = boto3.client('ses', region_name='eu-central-1') # add region to the client if needed
    # print(msg.as_string())

    print('To the well once more time to decide on?')

    # try:
    response = clientSES.send_raw_email(
        Source=from_address,
        Destinations=to_addresses,
        RawMessage={ 'Data':
                    msg.as_string()
        }
    )

    print('When its killing me, when will I really see')

    # except ClientError as e:
    #     print(e.resopnse['Error']['Mess'])

    #     status.append([0, e.resopnse['Error']['Mess']])

    #     # response = client.verify_email_identity(EmailAddress = from_address)
    #     # status.append([0,'Sender Address is not verified , sent mail for verification'])
    # else:
    #     print("Email sent! Message ID:"),
    #     print(response['MessageId'])
            
    status.append([0,'Notification Sent Successfully'])
    return {
        'data': status
    }
        
        
