from setuptools import setup, find_packages
from os import path

version = '1.0.1'
repo = 'SOCH-Download-CLI'

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'soch-download',
  install_requires=['requests', 'click', 'ksamsok'],
  scripts=['soch-download'],
  python_requires='>=3.4.0',
  version = version,
  description = 'SOCH Download CLI lets you do multithreaded batch downloads of Swedish Open Cultural Heritage(K-Samsök) records for offline processing and analytics.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Albin Larsson',
  author_email = 'albin.larsson@raa.se',
  url = 'https://github.com/riksantikvarieambetet/' + repo,
  download_url = 'https://github.com/riksantikvarieambetet/' + repo + '/tarball/' + version,
  keywords = ['SOCH', 'K-Samsök', 'heritage', 'cultural', 'CLI'],
  license='MIT',
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3 :: Only',
    'Intended Audience :: Developers',
    'Intended Audience :: Education'
  ]
)