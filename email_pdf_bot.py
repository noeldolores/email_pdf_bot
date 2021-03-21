#!/usr/bin/env python3

import emails
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    #print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    #print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    #print(pickle_file)

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
  # Create Service Instance
  CLIENT_SECRET_FILE = 'client_secret.json'
  API_NAME = 'gmail'
  API_VERSION = 'v1'
  SCOPES = ['https://mail.google.com/']
  
  service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
  
  # Send Email
  #userID= 'me'
  #receiver= 'noel.dolores@gmail.com'
  #subject= 'test3'
  #message= 'test3'
  #attachments = ['README.md']
  #emails.Send_Message_With_Attchments(service, userID, receiver, subject, message, attachments)
  
  # Check for Unread Emails
  message_info_list = emails.Get_Unread_Messages(service, 'me')
  for message in message_info_list:
  #  emails.Get_Attachments(service, 'me', message, "tmp/attachments/")
    info = emails.Get_Message_Info(service, 'me', message)
    print("sender: " + info[0])
    print("thread id: " + info[1])
    print("message id: " + info[2])
    userID= 'me'
    receiver= info[0]
    subject= info[3]
    message= 'test3'
    attachments = ['README.md']
    threadId = info[1]
    message_id = info[2]
    emails.Reply_With_Attchments(service, userID, receiver, subject, message, attachments, threadId, message_id)

if __name__ == "__main__":
  main()