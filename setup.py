import os

from setuptools import find_packages, setup


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as file:
        text = file.read()
    return text


def requirements():
    _requirements = set()
    for line in read('requirements.txt').split('\n'):
        if line.startswith('#') or \
                not line:
            continue
        _requirements.add(line)
    return list(_requirements)


setup(
    name='nlpreports',
    version='0.1',
    description='Util for analyze AWS NLP reports',
    author='Kirill Portenko',
    author_email='portenkok@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.md'),
    install_requires=requirements(),
    entry_points={
        'console_scripts': ['nlpreports = nlpreports.main:main']
    }
)
