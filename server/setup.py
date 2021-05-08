import os
import re

from __init__ import app_version

from setuptools import find_packages, setup

install_requires = [
    'Flask==1.1.2',
    'flask-cors==3.0.10',
    'gunicorn==20.0.4',
    'python-decouple==3.4',
    'matplotlib==3.3',
    'opencv-python==4.5.1.48',
    'pandas==1.0.3',
    'redis==3.5.3',
    'scikit-learn==0.24.1',
    'scipy==1.4.1',
    'seaborn==0.10.0',
    'yapsy==1.12.2',
]

setup(
    name='dolphin-segmentation',
    version=app_version(),
    description='Application for processing dolphin images.',
    platforms=['POSIX'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
)
