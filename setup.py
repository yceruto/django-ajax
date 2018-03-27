from setuptools import setup, find_packages
import os

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Dynamically calculate the version based on django.VERSION.
version = __import__('django_ajax').get_version()

setup(
    name='djangoajax',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,
    
    description='Powerful and easy AJAX framework for django applications.',
    long_description=README,
    
    # The project's main homepage.
    url='https://github.com/yceruto/django-ajax',
    
    # Author details
    author='Yonel Ceruto Glez',
    author_email='yonelceruto@gmail.com',
    
    license='MIT',
    
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    
    keywords='ajax django-ajax json',
    
    packages=find_packages(),

    platforms=['OS Independent'],
    
    install_requires=[
        'django>=2.0',
    ],

    include_package_data=True,
    zip_safe=False
)
