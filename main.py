"""
Created on Tue Nov 29 10:25:15 2022
@author: Alex
python -m pip install --upgrade pip
pip install PyPDF2
pip install pdf2image
pip install pytesseract
pip install Image

"""

import glob
import os
import time
from loguru import logger
from tkinter import filedialog
from src.parsertext import find_file, find_name
from src.pdf_file import PDF_File
from src.split import Split

logger.add(
    "log/info.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} {level} {name} {message}",
    rotation="10:00",
    compression="zip",
)


def main():
    dirpdf = filedialog.askdirectory()
    if dirpdf != "":
        begintime = time.time()

        find_file(dirpdf, "pdf")

        count_split = 0
        for file in glob.glob(dirpdf + "/split/*.pdf"):
            timefile = time.time()
            logger.info(f"Найден файл №{count_split}: {file}")
            image = PDF_File.pdf_to_image(file)
            text = PDF_File.image_to_text(image)
            os.remove(image)
            logger.info(f"Удален файл:", image)
            print(text)
            newfilename = find_name(text)
            if newfilename == "Введи в ручную":
                newfilename = f"Не распознал {count_split}.pdf"
            dirname, filename = os.path.split(file)
            newfile = os.path.join(dirname, newfilename)
            logger.info("Новое имя файла:", newfile)
            try:
                os.rename(file, newfile)
            except (FileExistsError, FileNotFoundError):
                newfilename = (
                    Split.file_name(Split.replace_flash(newfilename))
                    + f"_{count_split}_.pdf"
                )
                newfile = os.path.join(dirname, newfilename)
                os.rename(file, newfile)
            logger.info("Создан файл:", newfile)
            logger.info(
                f"Время обработки файла №{count_split} составило: {int(time.time() - timefile):.1f} сек"
            )
            count_split += 1
        logger.info(f"Найдено {count_split} файлов")
        t = time.time() - begintime
        logger.info(
            f"Время работы: {int(t/3600):0>2d}:{int(t%3600/60):0>2d}:{int(t%3600%60):0>2d}"
        )


if __name__ == "__main__":
    main()
