from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

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
      packages=['pyeti'],
      install_requires=[
          'requests',
          'logging',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      include_package_data=True,
      zip_safe=False)
