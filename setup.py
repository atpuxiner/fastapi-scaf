"""
@author axiner
@version v1.0.0
@created 2024/7/29 22:22
@abstract
@description
@history
"""
import os
import re
import sys
from pathlib import Path
from shutil import rmtree

from pkg_resources import yield_lines
from setuptools import Command, setup

from versions import Versions

here = Path(__file__).absolute().parent

__verison__ = Versions.ALL[0][0]

with open('README.md', 'r', encoding='utf8') as f:
    long_description = f.read()
with open('requirements.txt', 'r', encoding='utf8') as f:
    install_requires = list(yield_lines(f.read()))


def update_version():
    """update version"""
    vfile = here.joinpath('fastapi_scaf/__init__.py').as_posix()
    with open(vfile, 'r', encoding='utf8') as f:
        file = f.read()
    with open(vfile, 'w', encoding='utf8', newline='\n') as f:
        file = re.sub(r'__version__ = "[\d.]+"', rf'__version__ = "{__verison__}"', file)
        f.write(file)


def bu():
    """build"""
    update_version()
    try:
        print('Removing previous builds...')
        rmtree(os.path.join(here, 'dist'))
        rmtree(os.path.join(here, 'build'))
        rmtree(os.path.join(here, 'fastapi_scaf.egg-info'))
    except OSError:
        pass
    print('Building Source or Wheel distribution...')
    # os.system('{0} setup.py sdist bdist_wheel'.format(sys.executable))
    os.system('{0} setup.py bdist_wheel'.format(sys.executable))


class BuildCommand(Command):
    """support setup.py build"""
    description = 'Build the package.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        bu()
        sys.exit()


class UploadCommand(Command):
    """support setup.py build&upload"""
    description = 'Build and upload the package.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        bu()
        print('Uploading the package to PyPI via Twine...')
        os.system('twine upload dist/*')
        sys.exit()


setup(
    version=__verison__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    cmdclass={
        'bu': BuildCommand,
        'up': UploadCommand,
    },
)
