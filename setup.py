import distutils.extension
from setuptools import setup

setup(
    name='testsystems_uibcdf',
    version='0.1.1',
    author='UIBCDF Lab',
    author_email='uibcdf@gmail.com',
    packages=['testsystems_uibcdf'],
    package_dir={'testsystems_uibcdf': 'testsystems_uibcdf'},
    package_data={'testsystems_uibcdf': ['pdbs/*.pdb']},
    url='http://uibcdf.org',
    download_url ='https://github.com/uibcdf/TestSystems_uibcdf',
    license='MIT',
    description="doc to be done",
    long_description="long doc to be done",
)
