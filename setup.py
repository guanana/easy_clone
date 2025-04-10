from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'Easy clone'
LONG_DESCRIPTION = 'Convenient utility to clone in a organised way'

# Setting up
setup(
    name="easy_clone",
    version=VERSION,
    author="guanana",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'easy_clone=easy_clone.main:run'
        ]
    },
    install_requires=["gitpython"],  # add any additional packages that
    keywords=['python', 'git', 'clone', 'gitpython'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ]
)
