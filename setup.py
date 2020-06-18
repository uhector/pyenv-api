from setuptools import find_packages, setup

from pyenvapi import __version__


with open('README.rst', 'r') as rm:
    long_description = rm.read()


setup(
    name='pyenv-api',
    version=__version__,
    license='MIT',
    author='Hector Ulacio',
    author_email='hectorulacior@gmail.com',
    description='A simple API for pyenv',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/ulacioh/pyenv-api',
    packages=find_packages(),
    keywords=[
        'pyenv',
        'version-management'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)