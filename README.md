# Makaron

A simple way to handle your version number.

Look at the homepage: [makaron.gitlab.io](http://makaron.gitlab.io/)

## Config

Makaron expect a `.makaronrc` file in the current working directory.
This file list the files where Makaron has to update the version number.

You have to give Makaron two information. First the file where is suposed to search.
Second a regex that will let him find the line where is the version number.

You can update version number with this format `major.minor.patch` with the following `.makaronrc` file.

```
version:
  - file: setup.py
    regex:
      all: "__version__ = .*"
```

You can also choose to store your version number in different line with the following `.makaronrc` file.

```
version:
  - file: setup.py
    regex:
      major: "major = .*\n"
      minor: "minor = .*\n"
      patch: "patch = .*\n"
```

You can also add several files to update, like so:

```
version:
  - file: setup.py
    regex:
      all: "__version__ = .*"
  - file: setup.py
    regex:
      major: "major = .*\n"
      minor: "minor = .*\n"
      patch: "patch = .*\n"
```

## Update version

Just type the name of the number you want to increase:

```bash
$ makaron major
```
or

```bash
$ makaron minor
```

or

```bash
$ makaron patch
```
