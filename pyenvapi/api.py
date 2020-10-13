import os
import platform

from subprocess import Popen, PIPE
from subprocess import CalledProcessError

from .exceptions import (
    NotInstalledError,
    PyenvError,
    PythonBuildError,
)


class PyenvAPI:
    """The PyenvAPI class implements an interface that lets it interact
    with pyenv through subprocess module.
    """

    if platform.system() == 'Windows':
        _PYENV_WIN = True
    else:
        _PYENV_WIN = False

    _COMMANDS = (
        # Subcommands
        'global',
        'install',
        'root',
        'uninstall',
        'versions',
        # Options
        '--force',
        '--list',
        '--verbose',
    )

    def __new__(cls):
        """Checks if pyenv is installed before return an object."""

        args = ['pyenv', 'root']

        try:
            if cls._PYENV_WIN:
                ps = Popen(args[0], stdout=PIPE, stderr=PIPE, shell=True)
            else:
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
        self._root = self._get_root_path()
        #: Directory path where all Python versions are installed.
        self._versions_path = os.path.join(self._root, 'versions')

    def _execute(self, args):
        """Executes all synchronous subprocess calls.
        
        :param args: list of subcommands and options.
        """

        assert isinstance(args, list) 

        for arg in args:
            if (arg not in self._COMMANDS and
                arg not in self.installed):
                raise PyenvError(f"Invalid command `{arg}'")

        args.insert(0, 'pyenv')
        
        if self._PYENV_WIN:
            ps = Popen(args, stdout=PIPE, stderr=PIPE, shell=True)
        else:
            ps = Popen(args, stdout=PIPE, stderr=PIPE)
        
        stdout, stderr = ps.communicate()
        returncode = ps.returncode

        return returncode, stdout, stderr

    def _get_root_path(self):
        """Returns the pyenv root directory path."""

        if self._PYENV_WIN:
            return os.getenv('PYENV')
        else:
            args = ['root']
            ps = self._execute(args)
            
            returncode, stdout, stderr = ps
            stdout = stdout.decode()

            return stdout.strip()

    @property
    def root(self):
        return self._root

    @property
    def installed(self):
        """Returns a tuple of all installed versions."""
        
        versions = []
        
        for directory in os.listdir(self._versions_path):
            
            full_path = os.path.join(self._versions_path, directory)
            
            if not os.path.islink(full_path):
                versions.append(directory)

        return tuple(versions)

    @property
    def available(self):
        """Returns a tuple of all available Python versions to install."""

        args = ['install', '--list']
        ps = self._execute(args)

        returncode, stdout, stderr = ps
        stdout = stdout.decode()
        
        # For pyenv-win:
        if self._PYENV_WIN:
            available_versions = stdout.split()[5:]
        else:
            # Positions 0 and 1 in stdout after apply split() are
            # 'Available' and 'versions:' strings.
            available_versions = stdout.split()[2:]

        return tuple(available_versions)

    @property
    def global_version(self):
        """Returns a tuple of the currently active Python versions.
        
        They are return in order of priority.
        
        If there is only one Python version set as global version,
        the returned tuple will contain a single element.
        """

        args = ['global']
        ps = self._execute(args)

        returncode, stdout, stderr = ps
        stdout = stdout.decode()

        global_versions = stdout.split()

        if ' '.join(global_versions) == 'no global version configured':
            global_versions = ['system']

        return tuple(global_versions)

    @global_version.setter
    def global_version(self, versions):
        """Sets a tuple/list of Python versions as global.

        :param versions: tuple/list of one or multiple Python versions.
        """

        assert isinstance(versions, (tuple, list))

        for version in versions:
            if version not in self.installed:
                raise PyenvError(f"version `{version}' not installed")

        args = ['global']
        args.extend(versions)
        self._execute(args)

    @global_version.deleter
    def global_version(self):
        """Overwrites '.pyenv/version' file."""

        with open(os.path.join(self._root, 'version'), 'w') as file:
            pass # Nothing here...

    def install(self, version, verbose=False, force=False):
        """Starts a Python version intallation in a new process.
        
        :param versions: a string of a valid Python version.
        :param verbose: print compilation status to stdout.
        :param force: install even if the version appears to be
                      installed already.
        :return: subprocess.Popen object.
        """
        
        args = ['pyenv', 'install', version]

        if verbose == True and self._PYENV_WIN == False:
            args.append('--verbose')

        if version in self.installed:
            if force == True:
                args.append('--force')
            else:
                raise PyenvError(f"`{self._versions_path}/{version}' already exists")
        else:
            if version not in self.available:
                raise PythonBuildError(f"`{version}' is not a valid version")

        if self._PYENV_WIN:
            return Popen(args, stdout=PIPE, stderr=PIPE, shell=True)
        else:
            return Popen(args, stdout=PIPE, stderr=PIPE)

    def uninstall(self, version):
        if version not in self.installed:
            raise PyenvError(f"version `{version}' not installed")

        args = ['uninstall', '--force', version]

        return self._execute(args)
