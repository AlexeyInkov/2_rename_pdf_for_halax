import glob
import os
import re

from loguru import logger

from src.config_data import settings
from src.split import split_pdf_pages

MONTHS = {
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


def find_file(dir_file, template):

    count_file = 0
    for filename in glob.glob(dir_file + "/**/*." + (template), recursive=True):
        logger.info(f"Найден файл: {filename}")
        target_dir = dir_file + r"/split"
        split_pdf_pages(filename, target_dir)
        count_file += 1
    logger.info(f"Найдено {count_file} файлов")


def save_txt(text):
    if not os.path.exists("scan_text.txt"):
        method = "w"
    else:
        method = "a"
    with open("scan_text.txt", method) as file:
        file.write(text)
        file.write("------------------------------------------------")


def find_name(text):
    save_txt(text)
    regex_address = "|".join(
        (
            settings.regex_tgc,
            settings.regex_tek,
            settings.regex_pte,
            settings.regex_te,
            settings.regex_oth,
        )
    )
    match_address = re.findall(regex_address, text, re.MULTILINE)
    if match_address:
        address = match_address[0]
        logger.debug(f"Определил адрес: {address}")
        regex_period = settings.regex_period
        match_period = re.findall(regex_period, text, re.MULTILINE)
        if match_period:
            p = re.sub(r"\.", " ", match_period[0]).split()
            logger.debug(f"Определил дату: {p}")
            if p[0].isdigit():
                period = f"{p[-1]}{p[0]}"
            else:
                period = f"{p[-1]}{MONTHS.get(p[0].lower(), 'XX')}"
            logger.debug(f"Определил период: {period}")
        else:
            logger.debug(f"Не распознал дату")
            period = "XXXXXX"

        filename = f"{period}_{address}"
        filename = re.sub(r"\W", "_", filename)
        filename = re.sub(r"_{2,}", "_", filename)
        logger.debug(f"Новое имя файла: {filename}")
        return f"{filename}.pdf"
    else:
        logger.debug(f"Не распознал адрес")
        raise ValueError
