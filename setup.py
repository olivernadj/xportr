from setuptools import find_packages, setup

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="xportr",
    version="0.0.1",
    description="Lightweight Prometheus exporter",
    package_dir={"": "xportr"},
    packages=find_packages(where="xportr"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olivernadj/xportr",
    author="Oliver Nadj",
    author_email="mr.oliver.nadj@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: System :: Monitoring",
    ],
    install_requires=[""],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
