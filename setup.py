from setuptools import setup

setup(
   name='IDFYINSTRUMENTER',
   version='1.0',
   description='Idfy Instrumenter that takes logs and publishes them to RABBITMQ as well as the console',
   author='Prasann Patil',
   author_email='prasann@flairlabs.com',
   packages=['IDFYINSTRUMENTER'],  #same as name
   install_requires=['pika'], #external packages as dependencies
)

