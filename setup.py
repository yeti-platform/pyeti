from setuptools import setup

import pyeti

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pyeti',
      version=pyeti.__version__,
      description='Python bindings for Yeti\'s API',
      long_description=readme(),
      classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Threat Intelligence Plattform',
      ],
      keywords='yeti threat intel api',
      url='https://github.com/yeti-platform/pyeti',
      # author='To be defined',
      # author_email='none@example.com',
      license='BSD',
      packages=['pyeti'],
      install_requires=[
          'requests',
          'logging',
      ],
      # As soon there are tests defined
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      # Scripts we provide
      scripts=[
          'scripts/yeti_test_add_observable'
      ],
      #
      # Future hint for console scripts
      #entry_points={
      #    'console_scripts': ['funniest-joke=funniest.command_line:main'],
      #},
      include_package_data=True,
      zip_safe=False)
