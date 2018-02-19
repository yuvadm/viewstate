from setuptools import setup, find_packages

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='viewstate',
    version='0.0.1',
    description='.NET viewstate decoder',
    long_description=long_description,
    homepage='https://github.com/yuvadm/viewstate',
    author='Yuval Adam',
    packages=find_packages(exclude=['docs', 'tests']),
)
