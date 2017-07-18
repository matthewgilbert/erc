from setuptools import setup
import re

# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package#7071358
VERSIONFILE = "erc/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." %
                       (VERSIONFILE,))

LONG_DESCRIPTION = """
Implement risk parity optimization detailed in "On the Properties of
Equally-Weighted Risk Contributions Portfolios" by Maillard, Roncalli, and
Teiletche
"""

setup(name='erc',
      version=verstr,
      description='Risk parity optimization',
      long_description=LONG_DESCRIPTION,
      url='https://github.com/MatthewGilbert/erc',
      author='Matthew Gilbert',
      author_email='matthew.gilbert12@gmail.com',
      license='MIT',
      platforms='any',
      install_requires=['scipy', 'numpy'],
      packages=['erc', 'erc.tests'],
      test_suite='erc.tests',
      zip_safe=False)
