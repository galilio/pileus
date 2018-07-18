from setuptools import setup

setup(name = 'pileus',
    version = '0.1',
    description = 'api gateway based on nameko and bottle',
    author = 'XiaoYuming',
    author_email = 'xiaoyuming@bayesba.com',
    packages = ['pileus'],
    install_requires = ['nameko', 'bottle'])