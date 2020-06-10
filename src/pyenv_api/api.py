import os
from subprocess import run

from commands import (
    FORCE,
    GLOBAL,
    INSTALL,
    LIST,
    PYENV,
    ROOT,
    UNINSTALL,
    VERSION,
    VERSIONS,
    VERBOSE
)


class PyenvAPI(object):
    """The PyenvAPI class implements an interface that lets it interact
    with pyenv through subprocess module.
    """

    def __new__(cls):
        """Check if pyenv is installed.
        
        If it's installed, returns a `PyenvAPI` object.
        """

        check_pyenv = run([PYENV, ROOT], capture_output=True)

        if check_pyenv.returncode == 0:
            return super().__new__(cls)
        else:
            return None

    def __init__(self):
        #: Pyenv root directory path.
        self._root_dir = PyenvAPI._get_root_dir()

        #: Directory path where all Python versions are installed.
        self._versions_dir = os.path.join(self._root_dir, 'versions')

    @classmethod
    def _get_root_dir(cls) -> str:
        """Return the pyenv root directory"""

        ps = run([PYENV, ROOT], capture_output=True, text=True)

        stdout = ps.stdout

        return stdout.strip()
