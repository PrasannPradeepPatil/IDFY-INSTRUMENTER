from setuptools import setup

setup(
   name='Instrumenter',
   version='1.0',
   description='Idfy Instrumenter that takes logs and publishes them to RABBITMQ as well as the console',
   author='Prasann Patil',
   author_email='prasann@flairlabs.com',
   packages=['Instrumenter'],  #same as name
   install_requires=['pika', 'sys', 'json','os','datetime','threading','uuid'], #external packages as dependencies
)

