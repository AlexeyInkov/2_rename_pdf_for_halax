"""
python -m pip install --upgrade pip
pip install PyPDF2
pip install pdf2image
pip install pytesseract
pip install Image
"""

import glob
import os
import time
import uuid
from tkinter import filedialog

from loguru import logger

from src.parsertext import find_file, find_name
from src.pdf_file import PDFfile
from src.split import split_file_name

logger.add(
    "log/info.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} {level} {name} {message}",
    rotation="10:00",
    compression="zip",
)


@logger.catch
def main():
    dir_pdf = filedialog.askdirectory()
    if dir_pdf != "":
        begin_time = time.time()

        find_file(dir_pdf, "pdf")

        count_split = 0
        for file in glob.glob(dir_pdf + "/split/*.pdf"):
            count_split += 1
            timefile = time.time()

            logger.info(f"Найден файл №{count_split}: {file}")

            pdf_file = PDFfile(file)

            for _ in range(4):
                try:
                    new_filename = find_name(pdf_file.text)
                except ValueError:
                    pdf_file.rotate_image()
                else:
                    break
            else:
                new_filename = f"Не распознал {count_split}.pdf"

            dir_name, _ = os.path.split(file)

            newfile = os.path.join(dir_name, new_filename)
            logger.info(f"Новое имя файла: {newfile}")

            try:
                os.rename(file, newfile)
            except (FileExistsError, FileNotFoundError):
                filename = split_file_name(new_filename)
                new_filename = f"{filename[1]}_{str(uuid.uuid4())[:6]}.{filename[2]}"

                newfile = os.path.join(dir_name, new_filename)
                os.rename(file, newfile)
            logger.info(f"Создан файл: {newfile}")
            logger.info(
                f"Время обработки файла №{count_split} составило: {int(time.time() - timefile):.1f} сек"
            )

        logger.info(f"Найдено {count_split} файлов")
        t = time.time() - begin_time
        logger.info(
            f"Время работы: {int(t/3600):0>2d}:{int(t%3600/60):0>2d}:{int(t%3600%60):0>2d}"
        )


if __name__ == "__main__":
    main()
