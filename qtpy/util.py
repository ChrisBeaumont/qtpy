def pretty_number(numbers):
    """Convert a list of numbers into a nice list of strings

    :param numbers: Numbers to convert
    :type numbers: List or other iterable of numbers

    :rtype: A list of strings
    """
    try:
        return [pretty_number(n) for n in numbers]
    except TypeError:
        pass

    n = numbers
    if n == 0:
        result = '0'
    elif (abs(n) < 1e-3) or (abs(n) > 1e3):
        result = "%0.3e" % n
    elif abs(int(n) - n) < 1e-3 and int(n) != 0:
        result = "%i" % n
    else:
        result = "%0.3f" % n
    if result.find('.') != -1:
        result = result.rstrip('0')

    return result
