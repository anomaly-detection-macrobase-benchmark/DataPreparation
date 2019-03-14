def format_size(num):
    for unit in ['','K']:
        if abs(num) < 1000:
            return "%d%s" % (num, unit)
        num /= 1000
    return "%d%s" % (num, 'M')
