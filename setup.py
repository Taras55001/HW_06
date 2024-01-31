'''setup file for pip clean_folder'''
from setuptools import setup, find_namespace_packages

setup(name='clean-folder',
      version='1.0.3',
      description='Very useful code',
      url='http://github.com/dummy_user/useful',
      author='fantomas',
      author_email='pleasedonottextme@example.com',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': [
          'clean-folder = clean_folder.clean:main']})
