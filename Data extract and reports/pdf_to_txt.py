# -*- coding: utf-8 -*-

# This script allows to convert several PDF-files from 
# specified directory into one TXT-file.
# Uses PDFMiner library

import os

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


def convert_pdf_to_txt(path , txt_file):  
    """
        Takes 'path', where PDF-file placed to read.
        Extracted from PDF-file data are collected to 'txt_file'
    """
    
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    
    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    with open(newfile, 'a') as f:
        f.write(text)
    return text


def read_folder(folder, txt_file):          
    """
        Takes 'folder', where are one or several PDF-files to read.
        Extracted data collects to single 'txt_file'
    """
    path_f = []
    for d, dirs, files in os.walk(folder):
        for f in files:
            path = os.path.join(d,f) 
            path_f.append(path) 
    for f in path_f:
        print f
        convert_pdf_to_txt(f, txt_file)
    print 'Done.'


# __________________________________________________________________________________

# This function call will join all PDF-files at 'C:\Python27\Acts_test' folder
# and convert them to one TXT-file 'first_test.txt'
if __name__ == "__main__":
    read_folder('C:\Python27\Acts_test', 'first_test.txt')                   







