class Bytecnt:
    """
    Utility class to get human readable byte counts.

    Not a very good design with having to instantiate in order to get
    the result.
    """

    @staticmethod
    def bytecnt_to_str(num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)
