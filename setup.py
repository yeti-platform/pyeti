"""Packaging tool for the Yeti python bindings and CLI utility."""

from setuptools import setup
from setuptools import find_packages


def readme():
    """Returns contents of README.md."""
    with open('README.md') as readme_fp:
        return readme_fp.read()

setup(name='pyeti',
      version="0.0.1",
      description='Python bindings for Yeti\'s API',
      long_description=readme(),
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Threat Intelligence Platform',
      ],
      keywords='yeti threat intel api',
      url='https://github.com/yeti-platform/pyeti',
      author='Yeti core developers',
      license='Apache',
      packages=find_packages(),
      install_requires=[
          'requests',
          'logging',
          'tqdm',
      ],
      test_suite='nose.collector',
      tests_require=[
          'nose',
          'nose-cover3'
      ],
      entry_points={
          'console_scripts': ['yeticli=pyeti.scripts.cli:main'],
      },
      include_package_data=True,
      zip_safe=False)
