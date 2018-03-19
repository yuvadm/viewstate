from pathlib import Path

from setuptools import setup, find_packages

with open(str(Path(__file__).resolve().parents[0] / 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='viewstate',
    author='Yuval Adam',
    author_email='_@yuv.al',
    version='0.3.1',
    description='.NET viewstate decoder',
    long_description=long_description,
    url='https://github.com/yuvadm/viewstate',
    license='MIT',
    python_requires='>=3.5.0',
    packages=find_packages(exclude=['docs', 'tests']),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
