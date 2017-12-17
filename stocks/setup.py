from setuptools import setup

setup(
   name='guru',
   version='0.1',
   description='A useful module',
   author='guru',
   author_email='guru@guru.com',
   packages=['app', 'gene', 'data', 'etl'],  #same as name
   install_requires=['tushare'], #external packages as dependencies

)