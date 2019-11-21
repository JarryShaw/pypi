# Dummy repository for PyPI registration

```
$ dummy --help
usage: dummy [-h] [-o OUTPUT] [-f] [-r] [-v] [-j JSON] [-y YAML] [-i INI]
             [-n NAME] [-m MODULE] [-M MODULE_NAME] [-V VERSION] [-a AUTHOR]
             [-A AUTHOR_EMAIL] [-t MAINTAINER] [-T MAINTAINER_EMAIL] [-u URL]

dummy package generator

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output folder
  -f, --force           force generation even if package exists
  -r, --raise           raise error at runtime instead of reinstall
  -v, --verbose         give more output; option is additive

File configuration:
  use configuration file to setup dummy package

  -j JSON, --json JSON  path to JSON format configuration file
  -y YAML, --yaml YAML  path to YAML format configuration file
  -i INI, --ini INI     path to INI format configuration file

Command configuration:
  use command line options to setup dummy package

  -n NAME, --name NAME  dummy package name
  -m MODULE, --module MODULE
                        package module name
  -M MODULE_NAME, --module-name MODULE_NAME
                        expected module name
  -V VERSION, --version VERSION
                        package version string
  -a AUTHOR, --author AUTHOR
                        author name
  -A AUTHOR_EMAIL, --author-email AUTHOR_EMAIL
                        author email
  -t MAINTAINER, --maintainer MAINTAINER
                        maintainer name
  -T MAINTAINER_EMAIL, --maintainer-email MAINTAINER_EMAIL
                        maintainer email
  -u URL, --url URL     project URL
```
