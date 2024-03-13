from xportr.utils import float_to_go_string


def sample_line(name: str, labels: dict, value: int | float, timestamp_ns: int = None):
    if labels:
        label_str = '{{{0}}}'.format(','.join(
            ['{}="{}"'.format(
                k, v.replace('\\', r'\\').replace('\n', r'\n').replace('"', r'\"'))
                for k, v in sorted(labels.items())]))
    else:
        label_str = ''
    timestamp = ''
    if timestamp_ns is not None:
        # Convert to milliseconds.
        timestamp = f' {int(float(timestamp_ns) / 1000):d}'
    return f'{name}{label_str} {float_to_go_string(value)}{timestamp}\n'
