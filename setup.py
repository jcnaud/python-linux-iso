# from setuptools import setup
#
# setup(name='linuxiso',
#       version='0.1dev',
#       description='Download, custom and deploy (virtualbox) iso on linux',
#       url='http://github.com/jcnaud/linuxiso',
#       author='Jean-Charles Naud',
#       author_email='jeancharles.naud@gmail.com',
#       license='Apache License, Version 2.0',
#       packages=['???'],
#       zip_safe=False)
#

from distutils.core import setup

setup(
    name='LinuxIso',
    version='0.1dev',
    description='Download, custom and deploy (virtualbox) iso on linux',
    url='http://github.com/jcnaud/linuxiso',
    author='Jean-Charles Naud',
    author_email='jeancharles.naud@gmail.com',
    packages=['linuxiso', ],
    license='Apache License, Version 2.0',
    long_description=open('README.rst').read(),
)
