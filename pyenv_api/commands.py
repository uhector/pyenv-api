"""The pyenv command delegates to subcommands based on its
first argument.
"""

# Main command
PYENV = 'pyenv' # Lists all available pyenv commands

# Subcommands
GLOBAL   = 'global' # Sets the global version of Python
INSTALL  = 'install' # Install a Python version
ROOT = 'root' # Display the pyenv's root directory
UNINSTALL = 'uninstall' # Uninstall a specific Python version
VERSION = 'version' # Displays the currently active Python version
VERSIONS = 'versions' # Lists all Python versions known to pyenv

# Options
FORCE = '--force' # Install even if the version appears to be installed already
LIST = '--list' # List all available versions
VERBOSE = '--verbose' # Verbose mode: print compilation status to stdout