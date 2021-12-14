from .celery import app
import os
from pathlib import Path
from typing import Text
from typing import Tuple
import textract
import pickle

@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def textract_from_file(file_path: Text, file_name: Text) -> Tuple[Text, bool]:

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"")

    def _extract_from_pdf(file_path):
        # Try with textract, normal mode
        content = textract.process(file_path, extension="pdf").decode().strip()
        ocr = False
        if not content:
            # If no results, try with "tesseract" method if it's a scanned pdf
            print.warning("No text could be extrated. Trying OCR...")
            content = (
                textract.process(file_path, extension="pdf", method="tesseract")
                .decode()
                .strip()
            )
            ocr = True

        return content, ocr

    def _extract_from_other(file_path):
        return textract.process(file_path, extension=file_extension).decode().strip()

    file_extension = Path(file_name).suffix.lower()

    if file_extension == ".pdf":
        return _extract_from_pdf(file_path)

    return _extract_from_other(file_path), False

@app.task(serializer='pickle')
def textract_from_raw_bytes(raw_bytes,write_file='testFiles/tmp.txt'):
    raw_data = pickle.loads(raw_bytes)

    with open(write_file, "w") as file:
        file.write(raw_data)
    
    result =  textract_from_file(write_file, write_file.split('/')[-1])
    os.remove(write_file)
    return result