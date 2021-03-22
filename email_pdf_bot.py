#!/usr/bin/env python3

import emails
import pickle
import os
from pathlib import Path
import shutil
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import pdf

global _path
_path = "/home/noel/Email PDF Bot/"

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    cred = None
    pickle_file = _path + f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'connection successful')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def main():
  CLIENT_SECRET_FILE = _path + "client_secret.json"
  API_NAME = 'gmail'
  API_VERSION = 'v1'
  SCOPES = ['https://mail.google.com/']
  service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

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
      
      message= "You sent me these files: "
      for file in os.listdir(temp_folder):
        message += '\n'+file

      # Combine PDFs
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
    print(len(message_info_list))

if __name__ == "__main__":
  main()