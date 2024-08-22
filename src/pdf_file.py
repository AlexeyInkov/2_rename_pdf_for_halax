import pytesseract as pt
from PIL import Image
from loguru import logger
from pdf2image import convert_from_path

from src.config_data import settings


class PDFfile:

    def __init__(self, input_pdf_path):
        self.pdf = input_pdf_path
        self.image = self.pdf_to_image()
        self.image_header = self.crop_image()
        self.text = self.image_to_text()

    def pdf_to_image(self):
        images = convert_from_path(self.pdf, 300, poppler_path=settings.poppler_path)
        for image in images:
            return image

    def crop_image(self):
        width, height = self.image.size
        image_header = self.image.crop(
            (0, 0, width, int(height * settings.height_header))
        )
        logger.debug(f"Обрезал картинку")
        return image_header

    def image_to_text(self):
        pt.pytesseract.tesseract_cmd = settings.tesseract
        text = pt.image_to_string(
            self.image_header,
            lang=settings.tesseract_lang,
            config=settings.tesseract_config,
        )
        logger.debug(f"распознал картинку")
        return text

    def rotate_image(self):
        self.image = self.image.rotate(90, expand=True, resample=Image.BICUBIC)
        logger.debug(f"повернул картинку")
        self.image_header = self.crop_image()
        self.text = self.image_to_text()
