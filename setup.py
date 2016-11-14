import re
import ast
import platform
from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('todooo/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

install_requirements = [
    'colored==1.3.2',
]

description = 'CLI Tool for managing lists'

setup(
    name='todooo-cli',
    url='https://github.com/dansackett/todooo',
    author='Dan Sackett',
    author_email='danesackett@gmail.com',
    version=version,
    install_requires=install_requirements,
    packages=find_packages(),
    include_package_data=True,
    package_data={'todooo': []},
    description=description,
    long_description=description,
    entry_points={
        'console_scripts': [
            'todooo = todooo:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
