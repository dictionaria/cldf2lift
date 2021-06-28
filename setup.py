from setuptools import setup, find_packages


setup(
    name='cldf2lift',
    version='0.1a',
    description='',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    author='Johannes Englisch',
    author_email='johannes.englisch@shh.mpg.de',
    url='',
    keywords='data linguistics',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pycldf',
        'pycountry',
    ],
    extras_require={
        'cldfbench': ['cldfbench'],
        'dev': ['flake8'],
        'test': [
            'tox',
            'pluggy',
            'pytest',
            'pytest-mock',
            'pytest-cov',
            'coverage',
        ],
    },
    entry_points={
        'console_scripts': ['cldf2lift=cldf2lift.__main__:main'],
        'cldfbench.commands': ['lift=cldf2lift.bench']
    },
    tests_require=[],
    test_suite="cldf2lift")
