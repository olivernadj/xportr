from setuptools import setup

with open("./README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="xportr",
    version="0.0.4",
    description="Lightweight Prometheus exporter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olivernadj/xportr",
    author="Oliver Nadj",
    author_email="mr.oliver.nadj@gmail.com",
    license="MIT",
    packages=[
        'xportr',
        'xportr.prometheus',
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: System :: Monitoring",
    ],
    install_requires=[""],
    extras_require={
        "dev": [
            "pytest>=8.0.2",
            "pytest-cov>=4.1.0",
            "twine>=4.0.2",
            "ruff==0.3.2",
        ],
    },
    python_requires=">=3.10",
)
