#!/usr/bin/env python3

import PyPDF2

def Combine_Pdfs(folder, attachment_list):
  """Reply to message with the new pdf attached.
        Args:
            folder: Absolute path to folder containing pdfs to combine.
            attachment_list: List that holds specific order of pdfs to combine.
    """
  writer = PyPDF2.PdfFileWriter()
  pdf_list = attachment_list
  files_to_close = []

  for pdf in pdf_list:
    if pdf.lower().endswith('.pdf'):
      try:
        to_add = open('{}{}'.format(folder, pdf), 'rb')
        files_to_close.append(to_add)
        to_add_reader = PyPDF2.PdfFileReader(to_add, strict=False)
      except PyPDF2.utils.PdfReadError:
        fixed = Fix_Pdf_Eof_Error(folder, pdf)
        to_add = open('{}{}'.format(folder, fixed), 'rb')
        files_to_close.append(to_add)
        to_add_reader = PyPDF2.PdfFileReader(to_add, strict=False)
      except:
        continue

      for pageNum in range(to_add_reader.numPages):
        pageObj = to_add_reader.getPage(pageNum)
        writer.addPage(pageObj)
    else:
      #print("Wrong file type (not .pdf) : " + pdf)
      return False, pdf


  new_pdf = open('{}new_pdf.pdf'.format(folder), 'wb')
  writer.write(new_pdf)
  for files in files_to_close:
    files.close()
  new_pdf.close()

  return True, new_pdf


def Fix_Pdf_Eof_Error(folder, pdf):
  """Reply to message with the new pdf attached.
        Args:
            folder: Absolute path to folder containing pdfs to combine.
            pdf: Pdf file to add EOF marker to.
    """
  fixed = 'fixed.pdf'
  with open(folder + pdf, 'rb') as p:
    txt = (p.readlines())

  # find the line position of the EOF
  for i, x in enumerate(txt[::-1]):
    if b'%%EOF' in x:
      actual_line = len(txt)-i
      break
  
  txtx = txt[:actual_line]

  with open(folder + fixed, 'wb') as f:
    f.writelines(txtx)
    f.close()

  return fixed