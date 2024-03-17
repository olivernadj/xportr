import math
import re

METRIC_NAME_RE = re.compile(r'^[a-zA-Z_:][a-zA-Z0-9_:]*$')
METRIC_LABEL_NAME_RE = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
RESERVED_METRIC_LABEL_NAME_RE = re.compile(r'^__.*$')


def float_to_go_string(d):
    d = float(d)
    if d == float("inf"):
        return '+Inf'
    if d == float("-inf"):
        return '-Inf'
    if math.isnan(d):
        return 'NaN'
    s = repr(d)
    dot = s.find('.')
    # Go switches to exponents sooner than Python.
    # We only need to care about positive values for le/quantile.
    if d > 0 and dot > 6:
        mantissa = f'{s[0]}.{s[1:dot]}{s[dot + 1:]}'.rstrip('0.')
        return f'{mantissa}e+0{dot - 1}'
    return s



def validate_metric_name(name: str):
    if not METRIC_NAME_RE.match(name):
        raise ValueError('Invalid metric name: ' + name)


def validate_label_name(label: str):
    if not METRIC_LABEL_NAME_RE.match(label):
        raise ValueError('Invalid label metric name: ' + label)
    if RESERVED_METRIC_LABEL_NAME_RE.match(label):
        raise ValueError('Reserved label metric name: ' + label)


def validate_label_names(labels: dict):
    for k, _ in labels.items():
        validate_label_name(k)
