from setuptools import setup, find_packages

setup(
    name="pylogxo",
    version="1.0.3",
    description="Extended logging utilities with color, rotation, and JSON output",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Log Maintainer",
    author_email="support@pylogx.example",
    url="https://github.com/example/pylogx",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.4",
    ],
    extras_require={
        "json": ["orjson>=3.8.0"],
        "full": ["colorama", "orjson", "requests"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Logging",
    ],
    python_requires=">=3.6",
)
