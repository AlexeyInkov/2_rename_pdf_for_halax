"""
Created on Wed Nov 30 21:21:16 2022

@author: Alex
"""

import glob

from loguru import logger

from src.pdf_file import PDF_File
from src.split import split_pdf_pages


def find_file(dir_file, template):

    count_file = 0
    for filename in glob.glob(dir_file + "/**/*." + (template), recursive=True):
        logger.info(f"Найден файл: {filename}")
        target_dir = dir_file + r"/split"
        split_pdf_pages(filename, target_dir)
        count_file += 1
    logger.info(f"Найдено {count_file} файлов")


def find_name(text):
    months = {
        "январь": "01",
        "февраль": "02",
        "март": "03",
        "апрель": "04",
        "май": "05",
        "июнь": "06",
        "июль": "07",
        "август": "08",
        "сентябрь": "09",
        "октябрь": "10",
        "ноябрь": "11",
        "декабрь": "12",
    }
    lst = text.split()
    print(lst)
    try:
        p = lst.index("за", 0, 30)
        m = str(lst[p + 1]).lower()
        try:
            period = str(lst[p + 2]) + str(months[m])
        except KeyError:
            period = str(lst[p + 2]) + "XX"
    except ValueError or UnboundLocalError:
        p = 0
        period = "По часовой 90"

    #    print(period)
    try:
        an = lst.index("Адрес:", 0, 50)
        try:
            ak1 = lst.index("Телефон:", an)
        except ValueError:
            ak1 = 1000
        try:
            ak2 = lst.index("Строит.адрес:", an)
        except ValueError:
            ak2 = 1000
        try:
            ak3 = lst.index("Код", an)
        except ValueError:
            ak3 = 1000

        if ak1 < ak2 and ak1 < ak3:
            tso = "ТЭ"
            ak = ak1
        elif ak2 < ak3:
            tso = "ТЭК"
            ak = ak2
        else:
            tso = "ПТЭ"
            ak = ak3
        print(f"(Find.Find_name): период {p}, адрес {an}-{ak}({ak1}, {ak2}, {ak3})")
        if ak - an > 15:
            newfilename = "Введи в ручную"
        else:
            adres = (
                str(lst[an + 1])
                .replace(".", "")
                .replace(",", "")
                .replace(":", "")
                .replace("=", "")
                .replace("?", "")
                .replace("!", "")
                .replace("|", "")
                .replace('"', "")
                .replace(">", "")
                .replace("<", "")
            )
            for i in range(an + 2, ak):
                adres += "_" + str(lst[i]).replace(".", "").replace(",", "").replace(
                    ":", ""
                ).replace("=", "").replace("?", "").replace("!", "").replace(
                    "|", ""
                ).replace(
                    '"', ""
                ).replace(
                    ">", ""
                ).replace(
                    "<", ""
                )
            #    print(adres)
            newfilename = f"{tso}_{period}_{adres[0:50]}.pdf"
    except ValueError or UnboundLocalError:
        newfilename = "Введи в ручную"
    logger.info(f"Новое имя: {newfilename}")
    return newfilename


# dir_file = 'C:/Users/Alex/Documents/Python/Project/pdf/2211'
# template = 'pdf'
# Find.Find_file(dir_file, template)
