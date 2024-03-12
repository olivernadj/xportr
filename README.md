<img src="https://raw.githubusercontent.com/olivernadj/xportr/main/xportr.png" width="386" height="120" alt="logo"/>

-----------------

# xportr: Lightweight Prometheus exporter

| | |
| --- | --- |
| Testing | [![CI - Test](https://github.com/olivernadj/xportr/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/olivernadj/xportr/actions/workflows/unit-tests.yml) [![Coverage](https://codecov.io/github/olivernadj/xportr/coverage.svg?branch=main)](https://codecov.io/gh/olivernadj/xportr) |
| Package | [![PyPI Latest Release](https://img.shields.io/pypi/v/xportr.svg)](https://pypi.org/project/xportr/) |


It is an R&D hobby project to gain better understanding of [The official Python client](https://github.com/prometheus/client_python) 

Aimed to be minimalistic.

---
### Glossary

 - granular - resembling or consisting of small grains or particles. a measure of the number of elements of the set
 - cardinality - it is the number of unique attributes or entities observed for a given metric
 - sample - is a singe observation point for a given entity

### Model
```txt
MetricPool[Metric]
  - cardinal[Entity]
    - samples[Sample]
```