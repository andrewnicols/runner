import logging
import pprint

def getLogger():
    return logging.getLogger(__name__)

def setupLogger():
    debuglevel = logging.DEBUG

    logging.basicConfig(format='%(asctime)s\t%(name)s (%(levelname)s): %(message)s')

    logger = getLogger()
    logger.setLevel(debuglevel)
