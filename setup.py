import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-database-view',
    version='0.2.0',
    packages=['dbview'],
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
    include_package_data=True,
    license='MIT',
    description='A simple Django app to handle database views.',
    url='https://github.com/manuelnaranjo/django-database-view',
    author='Manuel F. Naranjo',
    author_email='naranjo.manuel@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
