import os
from subprocess import run, Popen, PIPE

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
    def available_verions(self) -> list:
        """Returns a list of all available Python versions to install"""

        ps = run([PYENV, INSTALL, LIST], capture_output=True, text=True)

        stdout = ps.stdout
        
        return stdout.split()[2:]

    @property
    def global_version(self) -> list:
        """Returns a list of the currently active Python versions
        
        They are return in order of priority."""

        ps = run([PYENV, GLOBAL], capture_output=True, text=True)

        stdout = ps.stdout
        
        return stdout.split()

    @global_version.setter
    def global_version(self, versions):
        assert isinstance(versions, (tuple, list))

        for version in versions:
            if version not in self.installed_versions:
                raise Exception(f"pyenv: version `{version}' not installed")

        command = [PYENV, GLOBAL] + list(versions)

        ps = run(command, capture_output=True, text=True)

    @global_version.deleter
    def global_version(self):
        """Overwrites 'version' pyenv file"""
        with open(os.path.join(self._root_dir, 'version'), 'w') as file:
            file.write('')

    def install(self, version, **kwargs) -> object:
        command = [PYENV, INSTALL, version]

        if kwargs.get('verbose', None):
            command += [VERBOSE]

        if version in self.installed_versions:
            if kwargs.get('force', None):
                command += [FORCE]
            else:
                raise Exception(f"pyenv: {self._versions_dir}/{version} already exists")
        else:
            if version not in self.available_verions:
                raise Exception(f"python-build: definition not found: {version}")

        return Popen(command, stdout=PIPE, stderr=PIPE)

    def uninstall(self, version):
        if version not in self.installed_versions:
            raise Exception(f"pyenv: version `{version}' not installed")
        
        ps = run([PYENV, UNINSTALL, FORCE, version], capture_output=True, text=True)

    @classmethod
    def _get_root_dir(cls) -> str:
        """Return the pyenv root directory"""

        ps = run([PYENV, ROOT], capture_output=True, text=True)

        stdout = ps.stdout

        return stdout.strip()
