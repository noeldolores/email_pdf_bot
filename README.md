A Python script that monitors an email address for messages with PDF attachmnets. If detected, the script will combine all
PDFs, in listed order, and reply to the message with the combined PDF attached.<br/><br/>


Problem:<br/>
<ol>
<li>At my workplace there are multiple printouts/handouts/etc that must be provided to patients for various provided services.</li>
<li>These are updated frequently, and would be more efficient for printing, sorting, and handing out as a single printable file.</li>
<li>Internally, there is very limited access to external websites/online tools.</li>
</ol>

Solution:<br/>
<ol>
<li>Use email as a workaround.</li>
<li>Create an email address to which you can send PDF files, and receive them back combined.</li>
</ol><br/>


This utilizes the Gmail API:<br/>
https://developers.google.com/gmail/api/quickstart/python<br/>


Try it out:<br/>
python.pdf.combine@gmail.com