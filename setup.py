import os
import sys

sys.path.append ('planetarium')
import __base__

from setuptools import setup

def read (*paths):
	with open (os.path.join (*paths), 'r') as aFile:
		return aFile.read()

setup (
	name = 'Planetarium',
	version = __base__.pl_version,
	description = 'A Python / React planetarium in the brower, using Transcrypt and Pyact',
	long_description = (
		read ('README.rst') + '\n\n' +
		read ('planetarium/license_reference.txt')
	),
	keywords = ['planetarium', 'transcrypt', 'pyact', 'numscrypt', 'react', 'python', 'browser'],
	url = 'https://github.com/QQuick/Planetarium',	
	license = 'Apache 2.0',
	author = 'Jacques de Hooge',
	author_email = 'jacques.de.hooge@qquick.org',
	packages = ['planetarium'],
	install_requires = [
		'transcrypt',
        'pyact',
        'numscrypt'
	],
	include_package_data = True,
	classifiers = [
		'Development Status :: 1 - Planning',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: Apache Software License',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3.9',
	],
)
