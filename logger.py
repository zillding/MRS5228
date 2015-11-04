import logging
from time import gmtime, strftime

output_file_name = strftime('%Y%m%d-%H%M%S', gmtime()) + '.log'

# create logger
logger = logging.getLogger('MRS5228')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(output_file_name)
# create console handler with a higher log level
ch = logging.StreamHandler()
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

def critical(s):
	logger.critical(s)

def error(s):
	logger.error(s)

def warning(s):
	logger.warning(s)

def info(s):
	logger.info(s)

def debug(s):
	logger.debug(s)
