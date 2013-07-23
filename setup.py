import os
from sys import argv
from setuptools import setup

try:
    if argv[1] == 'install':
        from os.path import join
        from distutils.sysconfig import get_python_lib
        from distutils.dir_util import copy_tree
        source = 'abalt_ajax'
        destination = join(get_python_lib(), 'abalt_ajax')
        copy_tree(source, destination)
except IndexError:
    pass

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Dynamically calculate the version based on django.VERSION.
version = __import__('abalt_ajax').get_version()

setup(
    name='abalt-django-ajax',
    version=version,
    packages=['abalt_ajax'],
    license='MIT',
    description='Powerful and easy AJAX toolkit for django applications. '
                'Contains ajax decorator, ajax middleware, shortcuts and more.',
    long_description=README,
    url='https://github.com/yceruto/abalt-django-ajax',
    author='Yonel Ceruto G.',
    author_email='yceruto@abalt.org',
    requires=['django'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
