# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 00:04:33 2022

@author: Alex
"""
import os

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
        i = 0
        for page in input_pdf.pages:
            output = PyPDF2.PdfWriter()
            output.add_page(page)
            if i == 0:
                file_name = os.path.join(
                    target_dir, ".".join(split_file_name(input_pdf_path)[1:])
                )
            else:
                file_name = os.path.join(
                    target_dir,
                    fname_fmt.format(
                        name=split_file_name(input_pdf_path)[1], num_page=i
                    ),
                )
            page_files.append(file_name)
            save_page_to_file(output, file_name)
            i += 1
