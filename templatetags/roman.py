from django.template import Library, TemplateSyntaxError

register = Library()

class RomanError(Exception): pass
class OutOfRangeError(RomanError): pass
class NotIntegerError(RomanError): pass

ROMAN_NUMBER_MAP = (('M',  1000),
                    ('CM', 900),
                    ('D',  500),
                    ('CD', 400),
                    ('C',  100),
                    ('XC', 90),
                    ('L',  50),
                    ('XL', 40),
                    ('X',  10),
                    ('IX', 9),
                    ('V',  5),
                    ('IV', 4),
                    ('I',  1))

def to_roman(n):
    """convert integer to Roman numeral"""
    if not isinstance(n, int):
        try:
            n = int(n)
        except ValueError:
            raise NotIntegerError, "non-integers cannot be converted"
    
    if not (0 < n < 4000):
        raise OutOfRangeError, "number out of range (must be 1..3999)"

    result = ""
    for numeral, integer in ROMAN_NUMBER_MAP:
        while n >= integer:
            result += numeral
            n -= integer
    return result

def roman_number(value):
    """
    Converts a number to its roman value

    Example usage::
        {{ 2007|roman_number }}
        {{ "2007"|roman_number }}
        {{ pub_date|date:"Y"|roman_number }}
    """
    try:
        value = to_roman(value)
    except RomanError, e:
        raise TemplateSyntaxError, "roman_number error: %s" % str(e)
    return value

register.filter('roman_number', roman_number)

