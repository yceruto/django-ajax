from setuptools import setup, find_packages
import os

CLASSIFIERS = [
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
]

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Dynamically calculate the version based on django.VERSION.
version = __import__('django_ajax').get_version()

setup(
    author='Yonel Ceruto Glez',
    author_email='yonelceruto@gmail.com',
    name='djangoajax',
    version=version,
    description='Powerful and easy AJAX framework for django applications.',
    long_description=README,
    url='https://github.com/yceruto/django-ajax',
    license='MIT License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'setuptools',
        'django>=1.3',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
