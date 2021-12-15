import logging
import time
import os
import sys
import coloredlogs

from src.tasks import add
from src.tasks import textract_from_file


logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger, level=logging.DEBUG)


def handle_result(result, func_name):
    while not result.ready():
        logger.info(f"🕜️ Waiting for result from {func_name}...")
        time.sleep(0.5)

    return result.get(timeout=1)


def call_add(n, m):
    logger.info(f"📢 Calling add")
    result = add.delay(n, m)
    r = handle_result(result, "add")
    logger.info(f" > Result: {r}")


def call_extract_from_file_with_path(file_path: str):
    logger.info(f"📢 Calling extract_from_file")
    logger.debug(f"Rx: {file_path}")

    result = textract_from_file.delay(file_path=file_path)
    r = handle_result(result, "extract_from_file (path)")

    logger.info(f" > Result: {r}")


def call_extract_from_file_with_bytes(file_path: str):
    logger.info(f"📢 Calling extract_from_file")
    logger.debug(f"Rx: {file_path}")

    _, fname = os.path.split(file_path)
    with open(file_path, "rb") as f:
        result = textract_from_file.delay(file_bytes=f.read(), meta={"filename": fname})
    r = handle_result(result, "extract_from_file (bytes)")

    logger.info(f" > Result: {r}")


if __name__ == "__main__":

    input_file = sys.argv[1]

    call_add(40, 2)
    call_extract_from_file_with_path(input_file)
    call_extract_from_file_with_bytes(input_file)
