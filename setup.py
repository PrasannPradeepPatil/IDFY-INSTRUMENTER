import setuptools

setuptools.setup(
    name='idfy-instrumenter',
    version='0.0.1',
    author_email='prasann@flairlabs.com',
    packages=setuptools.find_packages(),  # same as name
    install_requires=['pika'],  # external packages as dependencies
)
