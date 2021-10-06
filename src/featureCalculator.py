from dateutil.parser import parse
from price_parser import Price

def is_date(s, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: s, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(s, fuzzy=fuzzy)
        return True

    except Exception:
        return False


def is_integer(s):
    """
    Return whether the string can be interpreted as an integer

    :param string: s, string to check for an integer
    """
    if len(s) == 0:
        return False
    elif s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def is_price(s):
    """
    Return whether the string can be interpreted as a price

    :param string: s, string to check for a price
    """
    return Price.fromstring(s).currency != None
