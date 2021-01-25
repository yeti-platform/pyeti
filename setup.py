"""Packaging tool for the Yeti python bindings and CLI utility."""

from setuptools import setup
from setuptools import find_packages

"""Packaging tool for the Yeti python bindings and CLI utility."""

from setuptools import setup
from setuptools import find_packages

"""Returns contents of README.md."""
with open("README.md", "r", encoding="utf-8") as readme_fp:
    long_description = readme_fp.read()

setup(name='pyeti-python',
      version="1.0",
      description='Revival version of pyeti, the API for Yeti Threat Intel Platform.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python :: 3',
      ],
      keywords='yeti threat intel api',
      url='https://github.com/yeti-platform/pyeti',
      author='Yeti core developers | packaged by Thomas Roccia @fr0gger_',
      license='Apache',
      packages=find_packages(),
      install_requires=[
          'requests',
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
      python_requires='>=3.6',
      zip_safe=False)
