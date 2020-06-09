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
