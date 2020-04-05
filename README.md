# gray

[![](https://badge.fury.io/py/gray.png)](http://badge.fury.io/py/gray)
[![](https://travis-ci.org/dizballanze/gray.png?branch=master)](https://travis-ci.org/dizballanze/gray)

Less uncompromising Python code formatter

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

## Features

* TODO

