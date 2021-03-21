#!/usr/bin/env python3

import base64
from apiclient import errors
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import re

def Get_Attachments(service, user_id, msg_id, store_dir): #working
    """Get and store attachment from Message with given id.
        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
                can be used to indicate the authenticated user.
            msg_id: ID of Message containing attachment.
            store_dir: The directory used to store attachments.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        parts = [message['payload']]
        while parts:
            part = parts.pop()
            if part.get('parts'):
                parts.extend(part['parts'])
            if part.get('filename'):
                if 'data' in part['body']:
                    file_data = base64.urlsafe_b64decode(part['body']['data'].encode('UTF-8'))
                    #self.stdout.write('FileData for %s, %s found! size: %s' % (message['id'], part['filename'], part['size']))
                elif 'attachmentId' in part['body']:
                    attachment = service.users().messages().attachments().get(
                        userId=user_id, messageId=message['id'], id=part['body']['attachmentId']
                    ).execute()
                    file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                    #self.stdout.write('FileData for %s, %s found! size: %s' % (message['id'], part['filename'], attachment['size']))
                else:
                    file_data = None
                if file_data:
                    #do some staff, e.g.
                    path = ''.join([store_dir, part['filename']])
                    with open(path, 'wb') as f:
                        f.write(file_data)
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def Send_Message_With_Attchments(service, userID, receiver, subject, message, attachments): #working
  # Create email message
  emailMsg = message
  mimeMessage = MIMEMultipart()
  mimeMessage['to'] = receiver
  mimeMessage['subject'] = subject
  mimeMessage.attach(MIMEText(emailMsg, 'plain'))
  
  # Attach files
  file_attachments = attachments

  for attachment in file_attachments:
      content_type, encoding = mimetypes.guess_type(attachment)
      main_type, sub_type = content_type.split('/', 1)
      file_name = os.path.basename(attachment)
  
      f = open(attachment, 'rb')
  
      myFile = MIMEBase(main_type, sub_type)
      myFile.set_payload(f.read())
      myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
      encoders.encode_base64(myFile)
  
      f.close()
  
      mimeMessage.attach(myFile)
  
  raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
  
  message = service.users().messages().send(
      userId=userID,
      body={'raw': raw_string}).execute()

def Reply_With_Attchments(service, userID, receiver, subject, message, attachments, threadId, message_id): #not working
  # Create email message
  emailMsg = message
  mimeMessage = MIMEMultipart()
  mimeMessage['to'] = receiver
  mimeMessage['subject'] = subject
  #mimeMessage['threadId'] = threadId
  #mimeMessage['In-Reply-To'] = message_id
  mimeMessage.add_header('In-Reply-To', message_id)
  mimeMessage.add_header('References', message_id)
  #mimeMessage['References'] = message_id
  mimeMessage.attach(MIMEText(emailMsg, 'plain'))
  
  # Attach files
  file_attachments = attachments

  for attachment in file_attachments:
      content_type, encoding = mimetypes.guess_type(attachment)
      main_type, sub_type = content_type.split('/', 1)
      file_name = os.path.basename(attachment)
  
      f = open(attachment, 'rb')
  
      myFile = MIMEBase(main_type, sub_type)
      myFile.set_payload(f.read())
      myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
      encoders.encode_base64(myFile)
  
      f.close()
  
      mimeMessage.attach(myFile)
  
  raw_string = {'raw':base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()}
  raw_string['threadId']=threadId
  
  message = service.users().messages().send(userId=userID, body=raw_string).execute()

def Get_Unread_Messages(service, userId): #working
  message_list = []
  message_ids = service.users().messages().list(userId=userId, labelIds='INBOX', alt="json", q='is:unread has:attachment').execute()

  for message in message_ids['messages']:
    #print(message)
    message_list.append(message['id'])

  return message_list

def Get_Message_Info(service, userId, message_id): #working
  message_info = service.users().messages().get(userId=userId, id=message_id).execute()

  sender_index = 16
  sender = re.search(r"[<](.*)[>]", message_info['payload']['headers'][sender_index]['value'])

  thread_id = message_info['threadId']

  message_id_index = 18
  message_id = re.search(r"[<](.*)[>]", message_info['payload']['headers'][message_id_index]['value'])

  subject_index = 19
  subject = message_info['payload']['headers'][subject_index]['value']

  info = (sender[1], thread_id, message_id[1], subject)
  return info