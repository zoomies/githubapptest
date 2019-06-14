import io

from setuptools import find_packages, setup

setup(
    name='percheck',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
