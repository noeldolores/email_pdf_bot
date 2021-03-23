#!/usr/bin/env python3

#import emails
#import pickle
import os
from pathlib import Path
import shutil
import gmail_service
import emails
import pdf

#global _path
#_path = "/home/noel/Email PDF Bot/"



def main():
  _path = "/home/noel/Email PDF Bot/"

  CLIENT_SECRET_FILE = _path + "client_secret.json"
  API_NAME = 'gmail'
  API_VERSION = 'v1'
  SCOPES = ['https://mail.google.com/']
  service = gmail_service.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

  userID= 'me'
  
  message_info_list = emails.Get_Unread_Messages(service, 'me')
  if len(message_info_list) > 0:
    for message in message_info_list:
      info = emails.Get_Message_Info(service, 'me', message)

      receiver= info[0]
      subject= info[1]
      threadId = info[2]
      message_id = info[3]
      
      # Downloads attachments to temp folder
      temp_folder = _path + "tmp/attachments/{}/".format(threadId)
      Path(temp_folder).mkdir(parents=True, exist_ok=True)
      emails.Get_Attachments(service, 'me', message, temp_folder)
      
      # Create message body and list files
      message= "You sent me these files: "
      for file in os.listdir(temp_folder):
        message += '\n'+file

      # Combine PDFs and and error messages to body
      new_pdf = pdf.combine_pdfs(temp_folder)
      if new_pdf[0] != False:
        attachments = temp_folder + 'new_pdf.pdf'
      else:
        attachments = None
        message += '\n\nAt least one file is not a PDF, including:\n{}'.format(new_pdf[1])
        message += '\n\nPlease resend the correct files'

      # Reply to and Mark Email as Read 
      emails.Reply_With_Attchments(service, userID, receiver, subject, message, attachments, threadId, message_id)
      
      emails.Mark_As_Read(service, userID, threadId)

      # Delete Temporary Files
      dir_path=Path(temp_folder)
      try:
        shutil.rmtree(dir_path)
      except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))
  else:
    print("No messages to process")

if __name__ == "__main__":
  main()