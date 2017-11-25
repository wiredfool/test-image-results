import sys
from setuptools import setup

setup(
    name='test-image-results',
    version='0.0.3',
    packages=['test_image_results'],
    url='http://github.com/wiredfool/test-image-results',
    license='MIT',
    author='Eric Soroos',
    author_email='eric@soroos.net',
    description='Upload test images to web service ',
    long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read(),
    install_requires=['requests>=2.0.0'],
    zip_safe=False,
    keywords=['Testing', 'image'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
