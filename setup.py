from distutils.core import setup
from pygf import __version__


setup(
    name='gfpy',
    version=__version__,
    description='GrowthForecast API client written in python',
    url='https://github.com/ReSTARTR/pygf',
    author='ReSTARTR',
    maintainer='ReSTARTR',
    keywords=['GrowthForecast', 'metrics'],
    packages=['pygf'],
    test_suite='tests',
    requires=['requests', 'pyyaml'],
)
