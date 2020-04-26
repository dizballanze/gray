# gray

[![](https://badge.fury.io/py/gray.png)](http://badge.fury.io/py/gray)
[![](https://travis-ci.org/dizballanze/gray.png?branch=master)](https://travis-ci.org/dizballanze/gray)

Less uncompromising Python code formatter.

Gray stands on the shoulders of giants:

- [isort](https://timothycrosley.github.io/isort/) - imports sorting and more
- [pyupgrade](https://github.com/asottile/pyupgrade) - automatically upgrades syntax for newer versions of Python
- [add-trailing-comma](https://github.com/asottile/add-trailing-comma)
- [unify](https://github.com/myint/unify) - unify quotes style

## Usage

```
usage:
        gray myapp.py
        gray myproj/ tests/
        gray --log-level debug --formatters isort,unify ~/app

Less uncompromising Python code formatter. Args that start with '--' (eg.
--log-level) can also be set in a config file (~/.gray or
/etc/gray.conf or ./gray.conf). Config file syntax allows: key=value,
flag=true, stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi).
If an arg is specified in more than one place, then commandline values
override config file values which override defaults.

positional arguments:
  paths                 Paths to format

optional arguments:
  -h, --help            show this help message and exit

Logging options:
  --log-level {debug,info,warning,error,fatal}
  --log-format {stream,color,json,syslog}

Formatters options:
  -f FORMATTERS, --formatters FORMATTERS
                        Enabled formatters separated by comma (default: add-
                        trailing-comma,isort,pyupgrade,unify)
```

## Git Hook

You can setup gray formatting before each commit with pre-commit git hook.
Add following file to `.git/hooks/pre-commit` and make it executable with
`chmod +x .git/hooks/pre-commit`.

```
#!/usr/bin/env python
from gray.hooks import git_pre_commit

exit(git_pre_commit(stop_on_modify=True))
```

If `stop_on_modify` argument is `True`, hook will prevent commit if there are
any unstaged changes in files you about to commit.

Otherwise, any unstaged changes in this files will be added to the index
by the hook.

## Features

* TODO

