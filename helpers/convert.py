import re
from loguru import logger


def file_shp_to_province(file_shp: str):
    if file_shp is not None:
        clear = re.sub(r"^BATAS_", "", file_shp).replace("_", " ")
        logger.info("Province clear: {}", clear)
        return clear
    return None
