from pathlib import Path
from setuptools import setup

here = Path(__file__).parent.absolute()

# Get the long description from the README file
with open(here / 'README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(name='envipath-api',
      version='0.3.0',
      description="wrapper for rest calls to envipath",
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Emanuel Schmid',
      author_email='schmide@ethz.ch',
      license='MIT',
      url='https://github.com/emanuel-schmid/envipath-api',
      packages=['envirest'],
      install_requires=['argparse', 'requests'],
      zip_safe=False)
