# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 00:04:33 2022

@author: Alex
"""
class Split():
    def File_name(input_pdf_path, ext = '.PDF'):
        input_pdf_path = Split.Replace_flash(input_pdf_path)
        a = input_pdf_path.split('/')
        name = str(a[-1]).split(ext)
        print('(Split.File_name) Имя без расширения: ', str(name[0]))
        return str(name[0])

    def Dir_name(input_pdf_path):
        input_pdf_path = Split.Replace_flash(input_pdf_path)
        a = input_pdf_path.split('/')
        path = str(a[0])
        for i in range(1, len(a)-1):
            path += '/' + str(a[i])
        print('(Split.Dir_name) Имя без расширения: ', path)
        return path
        
    
    def Replace_flash(input_pdf_path):
        input_pdf_path = input_pdf_path.replace('\\', '/')
        return input_pdf_path
    
    