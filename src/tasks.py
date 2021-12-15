import logging
import os
import coloredlogs
import tempfile
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Text
from typing import Tuple

import textract

from src.celery import app


logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger, level=logging.DEBUG)


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task(serializer="pickle")
def textract_from_file(
    file_bytes: Text = None, file_path: Text = None, meta: Dict[Text, Any] = None
) -> Tuple[Text, bool]:
    def _extract_from_pdf(file_path):
        # Try with textract, normal mode
        content = textract.process(file_path, extension="pdf").decode().strip()
        ocr = False
        if not content:
            # If no results, try with "tesseract" method if it's a scanned pdf
            logger.warning("No text could be extrated. Trying OCR...")
            content = (
                textract.process(file_path, extension="pdf", method="tesseract")
                .decode()
                .strip()
            )
            ocr = True

        return content, ocr

    def _extract_from_other(file_path):
        return textract.process(file_path, extension=file_extension).decode().strip()

    def extract(file_path, file_extension):
        if file_extension == ".pdf":
            return _extract_from_pdf(file_path)

        return _extract_from_other(file_path), False

    if file_path:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Given file: '{file_path}' doesn't exists!")

        _, fname = os.path.split(file_path)
        file_extension = Path(fname).suffix.lower()

        return extract(file_path, file_extension)

    if file_bytes:
        filename = meta.get("filename")
        if filename is None:
            raise ValueError(
                "file_bytes provided but no file valid metadata given. "
                "Pass 'metadata.filename' so we can guess the extension"
            )

        file_extension = Path(filename).suffix.lower()

        with tempfile.NamedTemporaryFile(suffix=file_extension, mode="wb") as f:
            f.write(file_bytes)
            logger.warning(f"FILE: {f.name}")

            return extract(f.name, file_extension)
