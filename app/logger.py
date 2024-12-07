import logging


def setup_logging(log_panel=None, log_filename='logs/synthmate_log.log'):
    logger = logging.getLogger('SynthMATE')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    if log_panel:
        log_handler = logging.StreamHandler(log_panel)
        log_handler.setFormatter(console_formatter)
        logger.addHandler(log_handler)

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(console_formatter)
    logger.addHandler(file_handler)

    return logger
