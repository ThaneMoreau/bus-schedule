from datetime import datetime, date


intervals = (
    ('weeks', 604800),
    ('days', 86400),
    ('hours', 3600),
    ('minutes', 60),
    ('seconds', 1),
    )


def display_time(seconds, granularity=2):
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


def difference(start, end):
    if start and end:
        try:
            diff = datetime.combine(
                date.today(), end) - datetime.combine(date.today(), start)
        except TypeError:
            diff = datetime.strptime(
                end, '%H:%M') - datetime.strptime(start, '%H:%M')
        return display_time(diff.seconds)
