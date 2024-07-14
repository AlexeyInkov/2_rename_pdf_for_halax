import PIL
import pytesseract as pt
from PIL import Image
from loguru import logger
from pdf2image import convert_from_path

from src.config_data import settings


class PDF_File:
    def __init__(self, input_pdf_path):
        self.pdf = input_pdf_path
        self.image = self.pdf_to_image()
        self.text = self.image_to_text()

    def pdf_to_image(self):
        images = convert_from_path(self.pdf, 300, poppler_path=settings.poppler_path)
        for image in images:
            return image

    def image_to_text(self):
        pt.pytesseract.tesseract_cmd = settings.tesseract
        text = pt.image_to_string(self.image, lang="rus")
        logger.debug(f"распознал картинку")
        return text

    def rotate_image(self):
        self.image = self.image.rotate(90, expand=True, resample=Image.BICUBIC)
        self.text = self.image_to_text()
        logger.debug(f"повернул картинку")
