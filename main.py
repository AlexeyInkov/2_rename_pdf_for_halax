"""
Created on Tue Nov 29 10:25:15 2022
@author: Alex
python -m pip install --upgrade pip
pip install PyPDF2
pip install pdf2image
pip install pytesseract
pip install Image
pip install
pip install
pip install
"""

import glob
import os
import time

from tkinter import filedialog
from Find import Find
from PDF_File import PDF_File
from Split import Split


dirpdf = filedialog.askdirectory()
if dirpdf != '':
    begintime = time.time()
    Find.Find_file(dirpdf, 'pdf')
    count_split = 0
    for file in glob.glob(dirpdf + '/split/*.pdf'):
        timefile = time.time()
        print(f"(main) Найден файл №{count_split}:", file)
        image = PDF_File.PDFtoImage(file)
        text = PDF_File.Image_to_text(image)
        os.remove(image)
        print(f"(main) Удален файл:", image)
        print(text)
        newfilename = Find.Find_name(text)
        if newfilename == 'Введи в ручную':
            newfilename = f'Не распознал {count_split}.pdf'
        dirname, filename = os.path.split(file)
        newfile = os.path.join(dirname, newfilename)
        print("(main) новое имя файла:", newfile)
        try:
            os.rename(file, newfile)
        except (FileExistsError, FileNotFoundError):
            newfilename = Split.File_name(Split.Replace_flash(newfilename)) + f'_{count_split}_.pdf'
            newfile = os.path.join(dirname, newfilename)
            os.rename(file, newfile)
        print("(main) создан файл:", newfile)
        print(f"(main) Время обработки файла №{count_split} составило: {int(time.time() - timefile):.1f} сек")
        count_split += 1
    print(f'(main) Найдено {count_split} файлов')
    t = time.time() - begintime
    print(f'(main) Время работы: {int(t/3600):0>2d}:{int(t%3600/60):0>2d}:{int(t%3600%60):0>2d}')
