from xportr import (
    float_to_go_string,
    Metric,
)


def format_sample_line(name: str, labels: dict, value: float, timestamp_ns: int = None) -> str:
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
        timestamp = f' {int(float(timestamp_ns) / 1000000):d}'
    return f'{name}{label_str} {float_to_go_string(value)}{timestamp}\n'


def generate_metric_with_cardinals(metric: Metric) -> str:
    name = metric.name
    documentation = metric.documentation.replace('\\', r'\\').replace('\n', r'\n')
    req = metric.requirements
    output = [
        f'# HELP {name} {documentation}\n',
        f'# TYPE {name} {metric.requirements.metric_type.value}\n']
    metric_labels_keys = metric.labels_w_default.keys()
    for labels, cardinal in metric.get_cardinals().items():
        cardinal_labels = dict(zip(metric_labels_keys, labels))
        for sample in cardinal.get():
            output.append(format_sample_line(
                name=metric.name,
                labels=cardinal_labels,
                value=sample[1],
                timestamp_ns=(sample[0] if req.timestamped else None),
            ))
    return ''.join(output) if len(output) > 2 else ''


def generate_all_metrics(metrics: dict[tuple, Metric]) -> str:
    output = []
    for _, metric in metrics.items():
        output.append(
            generate_metric_with_cardinals(metric)
        )
    return ''.join(output)
