"""
Created on Thu Dec  1 22:56:20 2022

@author: Alex
"""
import PyPDF2
import os
from pdf2image import convert_from_path
import pathlib
from pathlib import Path
from split import Split
import pytesseract as pt
from PIL import Image

from src.config_data import settings


class PDF_File():
    def Split_pdf_pages(input_pdf_path, target_dir, fname_fmt="{name}_{num_page:04d}.pdf"):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            print(f'(PDF_File.Split_pdf_pages) Создана папка {target_dir}')
        with open(input_pdf_path, "rb") as input_stream:
            input_pdf = PyPDF2.PdfReader(input_stream)
            print(f'(PDF_File.Split_pdf_pages) Открыт файл: ', input_pdf_path)
            page_files = []
            for i in range(0, len(input_pdf.pages)):
                output = PyPDF2.PdfWriter()
                output.add_page(input_pdf.pages[i])
                file_name = os.path.join(target_dir, fname_fmt.format(name=Split.File_name(input_pdf_path), num_page = i + 1))
                page_files.append(file_name)
                with open(file_name, "wb") as outputStream:
                    output.write(outputStream)
                    print(f'(PDF_File.Split_pdf_pages) Создан файл: ', file_name)
    
    def PDFtoImage(input_pdf_path):
        dirname, filename = os.path.split(input_pdf_path)
        images = convert_from_path(input_pdf_path, 300, poppler_path=settings.poppler_path)
        for image in images:
            imagename = f'{Split.File_name(filename)}.png'
            imagename=os.path.join(dirname, imagename)
            image.save(imagename)
            print(f'(PDF_File.PDFtoImage) Создан файл {imagename}')
        return imagename


    def Image_to_text(filename, tesseract=settings.tesseract):
        # Необходимо указать путь к программе teseract
        pt.pytesseract.tesseract_cmd = tesseract
        text = pt.image_to_string(Image.open(filename), lang='rus')
        return text



        #input_pdf_path = 'C:/Users/Alex/Documents/Python/Project/pdf/2210/1.pdf'
#target_dir = 'C:/Users/Alex/Documents/Python/Project/pdf/2210/new'
#PDF_File.Split_pdf_pages(input_pdf_path, target_dir)

#path = r'C:\YandexDisk\Python\Project\pdf\2210\1_.pdf'
##path = path.replace('/', '\\')
##
##dir_image = Split.Dir_name(path)
##print(dir_image)
#PDF_File.PDFtoImage(path)

#print(PDF_File.Image_to_text(r'H:\YandexDisk\Python\Project\pdf\1_0001.png'))

