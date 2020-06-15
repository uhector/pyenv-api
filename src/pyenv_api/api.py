import os
from subprocess import run, Popen, PIPE
from subprocess import CalledProcessError # Exception

from .commands import (
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

from .exceptions import (
    NotInstalledError,
    PyenvError,
    PythonBuildError
)


class PyenvAPI:
    """The PyenvAPI class implements an interface that lets it interact
    with pyenv through subprocess module.
    """

    def __new__(cls):
        """Check if pyenv is installed before return an object."""

        args = [PYENV, ROOT]

        try:
            ps = Popen(args, stdout=PIPE, stderr=PIPE)

            stdout, stderr = ps.communicate()
            returncode = ps.returncode

            if returncode != 0:
                raise CalledProcessError(returncode, ' '.join(args), (stdout, stderr))

        except FileNotFoundError:
            raise NotInstalledError('pyenv not installed on your system') from None
        else:
            return super().__new__(cls)

    def __init__(self):
        #: Pyenv root directory path.
        self._root_dir = self._get_root_dir()

        #: Directory path where all Python versions are installed.
        self._versions_dir = os.path.join(self._root_dir, 'versions')

    def _get_root_dir(self) -> str:
        """Return the pyenv root directory path."""

        args = [PYENV, ROOT]

        ps = Popen(args, stdout=PIPE, stderr=PIPE)
        
        stdout = ps.communicate()[0].decode()

        return stdout.strip()

    @property
    def installed_versions(self) -> list:
        """Returns a list of all installed versions"""
        
        versions = []
        
        for directory in os.listdir(self._versions_dir):
            
            full_path = os.path.join(self._versions_dir, directory)
            
            if not os.path.islink(full_path):
                versions.append(directory)

        return versions

    @property
    def available_versions(self) -> list:
        """Return a list of all available Python versions to install."""

        args = [PYENV, INSTALL, LIST]

        ps = Popen(args, stdout=PIPE, stderr=PIPE)

        stdout = ps.communicate()[0].decode()
        # Positions 0 and 1 in stdout after apply split() are
        # 'Available' and 'versions:' strings.
        return stdout.split()[2:]

    @property
    def global_version(self) -> list:
        """Return a list of the currently active Python versions.
        
        They are return in order of priority.
        
        If there is only one Python version set as global version,
        the returned list will contain a single element.
        """

        args = [PYENV, GLOBAL]

        ps = Popen(args, stdout=PIPE, stderr=PIPE)

        stdout = ps.communicate()[0].decode()
        
        return stdout.split()

    @global_version.setter
    def global_version(self, versions):
        """Set a list of Python versions as global.

        :param versions: a tuple or list of one or multiple Python versions.
        """

        assert isinstance(versions, (tuple, list))

        for version in versions:
            if version not in self.installed_versions:
                raise PyenvError(f"version `{version}' not installed")

        args = [PYENV, GLOBAL] + list(versions)
        
        Popen(args, stdout=PIPE, stderr=PIPE)

    @global_version.deleter
    def global_version(self):
        """Overwrites '.pyenv/version' file."""

        with open(os.path.join(self._root_dir, 'version'), 'w') as file:
            pass # Nothing here...

    def install(self, version, verbose=False, force=False) -> object:
        """Start a Python version intallation in a new process.

        return a subprocess.Popen object.
        
        :param versions: a string of a valid Python version.
        :param verbose: print compilation status to stdout.
        :param force: install even if the version appears to be
                      installed already.
        """
        
        args = [PYENV, INSTALL, version]

        if verbose == True:
            args += [VERBOSE]

        if version in self.installed_versions:
            if force == True:
                args += [FORCE]
            else:
                raise PyenvError(f"`{self._versions_dir}/{version}' already exists")
        else:
            if version not in self.available_versions:
                raise PythonBuildError(f"`{version}' is not a valid version")

        return Popen(args, stdout=PIPE, stderr=PIPE)

    def uninstall(self, version):
        if version not in self.installed_versions:
            raise PyenvError(f"version `{version}' not installed")

        args = [PYENV, UNINSTALL, FORCE, version]

        Popen(args, stdout=PIPE, stderr=PIPE)
