# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 00:04:33 2022

@author: Alex
"""
from loguru import logger


class Split:
    def file_name(input_pdf_path, ext=".PDF"):
        input_pdf_path = Split.replace_flash(input_pdf_path)
        a = input_pdf_path.split("/")
        name = str(a[-1]).split(ext)
        logger.info(f"Имя без расширения: {name[0]}")
        return str(name[0])

    def dir_name(input_pdf_path):
        input_pdf_path = Split.replace_flash(input_pdf_path)
        a = input_pdf_path.split("/")
        path = str(a[0])
        for i in range(1, len(a) - 1):
            path += "/" + str(a[i])
        logger.info(f"Имя без расширения: {path}")
        return path

    def replace_flash(input_pdf_path):
        input_pdf_path = input_pdf_path.replace("\\", "/")
        return input_pdf_path
