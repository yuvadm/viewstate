from pathlib import Path

from setuptools import setup, find_packages

with open(str(Path(__file__).resolve().parents[0] / 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='viewstate',
    version='0.1.0',
    description='.NET viewstate decoder',
    long_description=long_description,
    homepage='https://github.com/yuvadm/viewstate',
    author='Yuval Adam',
    packages=find_packages(exclude=['docs', 'tests']),
)
