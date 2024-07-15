# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 00:04:33 2022

@author: Alex
"""
import os
import uuid
import PyPDF2
from loguru import logger


def split_file_name(input_pdf_path, ext=".PDF"):
    dir_name, file_name = os.path.split(input_pdf_path)
    lst_name = file_name.split(".")
    ext = lst_name[-1]
    file_name = ".".join(lst_name[:-1])
    return dir_name, file_name, ext


def save_page_to_file(output, file_name):
    with open(file_name, "wb") as outputStream:
        output.write(outputStream)
        logger.info(f"Создан файл: {file_name}")


def split_pdf_pages(input_pdf_path, target_dir, fname_fmt="{name}_{num_page:04d}.pdf"):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        logger.info(f"Создана папка {target_dir}")
    with open(input_pdf_path, "rb") as input_stream:
        input_pdf = PyPDF2.PdfReader(input_stream)
        logger.info(f"Открыт файл: {input_pdf_path}")
        page_files = []
        for page in input_pdf.pages:
            output = PyPDF2.PdfWriter()
            output.add_page(page)
            file_name = os.path.join(target_dir, str(uuid.uuid4()) + ".pdf")

            page_files.append(file_name)
            save_page_to_file(output, file_name)
