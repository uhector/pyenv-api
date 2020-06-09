"""Like git, the pyenv command delegates to subcommands based on its
first argument.
"""

# Main command
PYENV = 'pyenv'

# Subcommands
GLOBAL   = 'global'
INSTALL  = 'install'
ROOT = 'root' 
UNINSTALL = 'uninstall'
VERSION = 'version'
VERSIONS = 'versions'

# Options
FORCE = '--force'
LIST = '--list'
VERBOSE = '--verbose'