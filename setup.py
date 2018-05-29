import distutils.extension
from setuptools import setup

DOCLINES = __doc__.split("\n")

setup(
    name='testsystems_uibcdf',
    version=__version__,
    author='UIBCDF Lab',
    author_email='uibcdf@gmail.com',
    packages=['testsystems_uibcdf'],
    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://uibcdf.org',
    download_url ='https://github.com/uibcdf/TestSystems_uibcdf'
    license='MIT',
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
)
