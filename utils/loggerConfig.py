import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(name)-12s] [%(levelname)-6s] - %(message)s',
                    datefmt='%m-%d %H:%M')


def getDefaultConfigLogger(moduleName="Computer vision based entry management system"):
    logger = logging.getLogger(moduleName)
    # console = logging.StreamHandler()
    # console.setLevel(logging.DEBUG)
    # logger.addHandler(console)
    return logger
