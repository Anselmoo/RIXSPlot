try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__authors__ = ['Anselm Hahn']
__license__ = 'MIT'
__version__ = '1.0'
__date__ = '12/09/2019'

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
	name='RIXSPlot',
	python_requires='>=3.6.0',
	version=__version__,
	packages=['test', 'RIXSPlot', 'Interface'],
	install_requires=required,
	url='https://github.com/Anselmoo/RIXSPlot',
	download_url='https://github.com/Anselmoo/RIXSPlot/releases',
	license=__license__,
	author=__authors__,
	author_email='Anselm.Hahn@gmail.com',
	description='RIXS-Plotting program for XAS- and XES-Cuts and further modifications',
	platforms=['MacOS :: MacOS X', 'Microsoft :: Windows','POSIX :: Linux'],
)
