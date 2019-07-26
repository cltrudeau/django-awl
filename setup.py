import os

from awl import __version__

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme).read()


SETUP_ARGS = dict(
    name='django-awl',
    version=__version__,
    description='Miscellaneous django tools',
    long_description=long_description,
    url='https://github.com/cltrudeau/django-awl',
    author='Christopher Trudeau',
    author_email='ctrudeau+pypi@arsensa.com',
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='django,state machine',
    test_suite="load_tests.get_suite",
    install_requires=[
        'Django>=1.11',
        'logthing>=0.10.1',
        'screwdriver>=0.11.0',
        'six>=1.11',
        'waelstow>=0.10.2',
    ],
    tests_require=[
        'mock>=2.0.0',
        'context-temp>=0.11.0',
    ]
)

if __name__ == '__main__':
    from setuptools import setup, find_packages

    SETUP_ARGS['packages'] = find_packages()
    setup(**SETUP_ARGS)
