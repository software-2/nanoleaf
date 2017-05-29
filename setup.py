from setuptools import setup
import subprocess

gitVersion = subprocess.check_output("git tag -l --points-at HEAD".split()).decode('UTF-8').strip()

setup(
  name = 'nanoleaf',
  packages = ['nanoleaf'],
  version = gitVersion,
  description = 'Python interface for Nanoleaf Aurora.',
  long_description=open('README.rst', 'r').read(),
  author = 'Anthony Bryan',
  author_email = 'projects@anthonybryan.net',
  url = 'https://github.com/software-2/nanoleaf',
  download_url = 'https://github.com/software-2/nanoleaf/archive/' + gitVersion + '.tar.gz',
  keywords = ['nanoleaf', 'aurora', 'lighting', 'openAPI'],
  classifiers = [
      'Topic :: Home Automation',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3'
  ],
)

