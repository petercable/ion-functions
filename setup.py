from setuptools import setup, find_packages
from distutils.extension import Extension

import numpy as np
# setuptools DWIM monkey-patch madness
# http://mail.python.org/pipermail/distutils-sig/2007-September/thread.html#8204
import sys

if 'setuptools.extension' in sys.modules:
    m = sys.modules['setuptools.extension']
    m.Extension.__dict__ = m._Extension.__dict__

packages = find_packages()

classifiers = ''' Intended Audience :: Science/Research
Intended Audience :: Developers
Intended Audience :: Education
Operating System :: OS Independent
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Education
Topic :: Software Development :: Libraries :: Python Modules'''

qc_extension_sources = ["ion_functions/qc/qc_extensions.pyx",
                        "extensions/stuck.c",
                        "extensions/spike.c",
                        "extensions/gradient.c",
                        "extensions/utils.c",
                        "extensions/time_utils.c", ]

qc_extension = Extension("ion_functions.qc.qc_extensions", qc_extension_sources,
                         include_dirs=[np.get_include(), "extensions/"], libraries=["m"])

wmm_extension_sources = ["ion_functions/data/wmm.pyx",
                         "extensions/GeomagnetismLibrary.c",
                         "extensions/wmm.c", ]

wmm_extension = Extension("ion_functions.data.wmm", wmm_extension_sources,
                          include_dirs=[np.get_include(), "extensions/"], libraries=["m"])

polycals_sources = ["ion_functions/data/polycals.pyx",
                    "extensions/polycals.c"]
polycals_extension = Extension("ion_functions.data.polycals", polycals_sources,
                               include_dirs=[np.get_include(), "extensions/"], libraries=["m"])

setup(name='ion-functions',
      version='2.1.1',
      description='Python Function collection for ION',
      long_description=open('README.md').read(),
      license='LICENSE.txt',
      author='Luke Campbell',
      author_email='lcampbell@asascience.com',
      url='https://github.com/ooici/ion-functions/',
      classifiers=classifiers.split('\n'),
      packages=packages,
      keywords=['oceanography', 'seawater'],
      ext_modules=[qc_extension, wmm_extension, polycals_extension],
      setup_requires=['setuptools_cython'],
      include_package_data=True,
      )
