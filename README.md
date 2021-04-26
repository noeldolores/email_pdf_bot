A Python script that monitors an email address for messages with PDF attachmnets. If detected, the script will combine all
PDFs, in listed order, and reply to the message with the combined PDF attached. 


Problem:
1. At my workplace there are multiple printouts/handouts/etc that must be provided to patients for various provided services.
2. These are updated frequently, and would be more efficient for printing, sorting, and handing out as a single printable file. 
3. Internally, there is very limited access to external websites/online tools.

Solution:
1. Use email as a workaround.
2. Create an email address to which you can send PDF files, and receive them back combined.


This utilizes the Gmail API: https://developers.google.com/gmail/api/quickstart/python


Try it out:
python.pdf.combine@gmail.com