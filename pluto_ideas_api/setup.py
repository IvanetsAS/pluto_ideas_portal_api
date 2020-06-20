from setuptools import setup

setup(
    name='Pluto Ideas Api',
    version='1.0',
    long_description=__doc__,
    packages=['pluto_ideas_api'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)