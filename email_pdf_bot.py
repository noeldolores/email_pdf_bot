#!/usr/bin/env python3

from pathlib import Path
import shutil
import gmail_service
import emails
import pdf


def main():
  _path = "/home/noel/Email PDF Bot/"
  
  # Connects to google gmail service
  CLIENT_SECRET_FILE = _path + "client_secret.json"
  API_NAME = 'gmail'
  API_VERSION = 'v1'
  SCOPES = ['https://mail.google.com/']
  service = gmail_service.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

  userID= 'me'
  
  #  Checks for and retrieves unread messages with attachments
  message_info_list = emails.Get_Unread_Messages(service, 'me')
  if len(message_info_list) > 0:
    for message in message_info_list:
      info = emails.Get_Message_Info(service, 'me', message)

      receiver= info[0]
      subject= info[1]
      threadId = info[2]
      message_id = info[3]
      attachment_list = info[4]
      ID = info[5]
      
      # Downloads attachments to temp folder
      temp_folder = _path + "tmp/attachments/{}/".format(threadId)
      Path(temp_folder).mkdir(parents=True, exist_ok=True)
      emails.Get_Attachments(service, 'me', message, temp_folder)
      
      # Create message body and list files
      message= "You sent me these files: "
      for item in attachment_list:
        message += '\n'+ item

      # Combine PDFs and add error messages to body
      new_pdf = pdf.combine_pdfs(temp_folder, attachment_list)
      if new_pdf[0] != False:
        attachments = temp_folder + 'new_pdf.pdf'
      else:
        attachments = None
        message += '\n\nAt least one file is not a PDF, including:\n{}'.format(new_pdf[1])
        message += '\n\nPlease resend the correct files'

      # Reply to Email
      emails.Reply_With_Attchments(service, userID, receiver, subject, message, attachments, threadId, message_id)
      
      # Permanently Delete Message
      emails.Delete_Message(service, userID, ID)
      
      # Delete Temporary Files
      dir_path=Path(temp_folder)
      try:
        shutil.rmtree(dir_path)
      except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))

      # Increment Use Tally
      with open(_path + 'tally.txt', 'r+') as t:
        tally = int(t.read()) + 1
        t.seek(0)
        t.write(str(tally))
  else:
    print("No messages to process")

if __name__ == "__main__":
  main()