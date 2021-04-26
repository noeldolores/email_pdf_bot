A Python script that monitors an email address for messages with PDF attachmnets. If detected, the script will combine all
PDFs, in listed order, and reply to the message with the combined PDF attached. 
<br/><br/>
Problem:<br/>
1) At my workplace there are multiple printouts/handouts/etc that must be provided to patients for various provided services.<br/>
2) These are updated frequently, and would be more efficient for printing, sorting, and handing out as a single printable file. <br/>
3) Internally, there is very limited access to external websites/online tools.
<br/>
Solution:<br/>
1) Use email as a workaround.<br/>
2) Create an email address to which you can send PDF files, and receive them back combined.
<br/><br/>
This utilizes the Gmail API:
<br/>
https://developers.google.com/gmail/api/quickstart/python
<br/><br/>
Try it out:
<br/>
python.pdf.combine@gmail.com