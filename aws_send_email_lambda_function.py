import json
import boto3
client = boto3.client("ses")


def lambda_handler(event,context):
    # print(event)
    status=[]
    row = event["data"][0] # gets the first 'row' from event data

    # row[0] ... row index
    from_address=row[1] # it's needed for AWS
    to_addresses=row[2]
    cc_addresses=row[3]
    bcc_addresses=row[4]
    
    subject=row[5]
    body_format=row[6]
    importance=row[7]
    sensitivity=row[8]
    body=row[9]
    file_attachments=row[10]
    #print('from_address: ' + str(from_address) + 'to_addresses: ' + str(to_addresses) + 'cc_addresses: ' + str(cc_addresses) + 'subject: ' + str(subject) + 'body: ' + str(body) + 'attachments: ' + str(attachments) + 'message: ' + str(content))
    
    # try:
    response=client.send_email(
            Source=from_address,
            Destination={
                "ToAddresses":to_addresses,
                "CcAddresses":cc_addresses,
                "BccAddresses":bcc_addresses},
            Message={"Subject":
                        {"Data": subject}, 
                        "Body": { body_format : {"Data": body}}
                    }
    )
    status.append([0,'Notification Sent Successfully'])
    # except:
    #     response = client.verify_email_identity(EmailAddress = from_address)
    #     status.append([0,'Sender Address is not verified , sent mail for verification'])
            
    return {
        'data': status
    }
        
        
