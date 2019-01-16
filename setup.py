from setuptools import setup
version = '1.0.0'
repo = 'SOCH Download CLI'

setup(
  name = 'soch-download',
  install_requires=['requests', 'click', 'ksamsok'],
  scripts=['soch-download'],
  python_requires='>=3.4.0',
  version = version,
  description = 'SOCH Download CLI lets you do multithreaded batch downloads of Swedish Open Cultural Heritage(K-Samsök) records for offline processing and analytics.',
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