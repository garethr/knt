from setuptools import setup

setup(
    name='knt',
    author='Gareth Rushgrove',
    author_email='gareth@morethanseven.net',
    version='0.1.0',
    license='Apache License 2.0',
    packages=['knt',],
    install_requires=[
        'requests',
        'pyyaml',
        'tabulate',
        'pygments',
	'click',
    ],
    tests_require=[

    ],
    entry_points={
        'console_scripts': [
            'knt = knt.command:cli'
       ]
    },
    keywords = 'kubernetes, knative',
    description = 'A utility to explore and install build templates for Knative Build.',
    url = "https://github.com/garethr/knt/",
)
