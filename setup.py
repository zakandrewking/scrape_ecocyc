try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='scrape_ecocyc',
    version='0.1.0',
    packages=['scrape_ecocyc'],
    install_requires=['Scrapy>=1.0.5'],
)
