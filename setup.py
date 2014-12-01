try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

config = {
  'name': 'async_pubsub',
  'description': 'Asynchronous pub/sub in Python', 
  'author': 'Shal Dengeki',
  'author_email': 'shaldengeki@gmail.com', 
  'license': 'LICENSE',
  'url': 'URL', 
  'download_url': 'DOWNLOAD_URL', 
  'version': '0.1', 
  'install_requires': ['collections', 'multiprocessing'],
  'tests_require': ['nose'], 
  'packages': ['async_pubsub']
}

setup(**config)