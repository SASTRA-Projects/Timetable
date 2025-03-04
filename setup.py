from setuptools import setup, find_packages
from pathlib import Path

def load_requirements(filename):
    with open(filename) as file:
        return file.read().splitlines()

setup(
    name="SASTRA",
    version="0.1.1a1",
    author="Harikrishna Srinivasan",
    license="Apache-2.0",
    packages=find_packages(),
    install_requires=load_requirements("requirements.txt"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Framework :: Flask"
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "your-command = app:run",
        ]
    },
    long_description="Working on it..."
)
