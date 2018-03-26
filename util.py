import logging


class Util():

    @staticmethod
    def setup_logging(prefix='', debug=False):
        """
	Setup logging and return logger.
	"""
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(format="%(message)s")

        return logging.getLogger(prefix)
