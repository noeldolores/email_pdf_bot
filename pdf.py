#!/usr/bin/env python3

import PyPDF2
import os

def combine_pdfs(folder):
  is_pdf = True
  writer = PyPDF2.PdfFileWriter()
  pdf_list = os.listdir(folder)
  files_to_close = []

  for pdf in pdf_list:
    if pdf.lower().endswith('.pdf'):
      try:
        to_add = open('{}{}'.format(folder, pdf), 'rb')
        files_to_close.append(to_add)
        to_add_reader = PyPDF2.PdfFileReader(to_add, strict=False)
      except PyPDF2.utils.PdfReadError:
        fixed = fix_pdf_eof_error(folder, pdf)
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
      is_pdf = False
      return False, pdf


  new_pdf = open('{}new_pdf.pdf'.format(folder), 'wb')
  writer.write(new_pdf)
  for files in files_to_close:
    files.close()
  new_pdf.close()

  return True, new_pdf


def fix_pdf_eof_error(folder, pdf):
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