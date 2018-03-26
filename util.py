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

    @staticmethod
    def bytecnt_to_str(num, suffix='B'):
        """
        Return human readable representation of byte count"
        """
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)
