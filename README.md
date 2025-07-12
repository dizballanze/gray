# gray

[![Package Version](https://badge.fury.io/py/gray.svg)](http://badge.fury.io/py/gray)
[![Build Status](https://travis-ci.org/dizballanze/gray.svg?branch=master)](https://travis-ci.org/dizballanze/gray)

Less uncompromising Python code formatter.

Gray stands on the shoulders of giants:

- [isort](https://timothycrosley.github.io/isort/) - imports sorting and more
- [pyupgrade](https://github.com/asottile/pyupgrade) - automatically upgrades syntax for newer versions of Python
- [autoflake](https://github.com/myint/autoflake) - remove unused imports and variables
- [add-trailing-comma](https://github.com/asottile/add-trailing-comma)
- [trim](https://github.com/myint/trim) - remove trailing whitespaces
- [string_fixer](https://github.com/Crozzers/string-fixer) - unify quotes style
- [fixit](https://github.com/Instagram/Fixit) - various code formatters on LibCST
- [black](https://github.com/psf/black) - optional - the uncompromising Python code formatter

## Usage

```
usage:
            gray myapp.py
            gray myproj/ tests/
            gray --log-level debug --formatters isort,string_fixer ~/app


Less uncompromising Python code formatter.

positional arguments:
  paths                 Paths to format (default: (PosixPath('.'),))

options:
  -h, --help            show this help message and exit
  --exclude EXCLUDE     A regular expression matching files and directories that should be excluded from formatting. Passing an explicit empty value means not paths get excluded. Use '/' as directory separator, including on Windows. [default: (.*/)?(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|venv|\.svn|_build|buck-
                        out|build|dist|__pypackages__)$] (default: (.*/)?(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|venv|\.svn|_build|buck-out|build|dist|__pypackages__)$)
  --extend-exclude EXTEND_EXCLUDE
                        An additional regular expression to use besides --exclude. This allows to keep the default regex from --exclude. (default: None)
  --pool-size POOL_SIZE
                        process pool size (default: 8)
  --do-not-detect-venv  Don't try to detect virtualenv (default: False)

Logging options:
  --log-level {debug,info,warning,error,fatal}

Formatters options:
  -f FORMATTERS, --formatters FORMATTERS
                        Enabled formatters separated by comma (optional: black) (default: add-trailing-comma,autoflake,fixit,isort,pyupgrade,string_fixer,trim)
  --min-python-version MIN_PYTHON_VERSION
                        Minimum python version to support (default: (3, 10))

pyupgrade options:
  --pyupgrade-keep-percent-format PYUPGRADE_KEEP_PERCENT_FORMAT
                        Do not upgrade percent formatted strings to f-strings (default: False)
  --pyupgrade-keep-mock PYUPGRADE_KEEP_MOCK
                        Disable rewrite of mock imports (default: False)
  --pyupgrade-keep-runtime-typing PYUPGRADE_KEEP_RUNTIME_TYPING
                        Disable pep 585 typing rewrites (default: False)

string_fixer options:
  --string-fixer-quote {single,double}
                        preferred quote (default: double)

isort options:
  --isort-profile ISORT_PROFILE
                        Base profile type to use for configuration. (default: None)
  --isort-line-length ISORT_LINE_LENGTH
                        The max length of an import line (used for wrapping long imports) (default: 80)
  --isort-wrap-length ISORT_WRAP_LENGTH
                        Specifies how long lines that are wrapped should be, if not set line_length is used. NOTE: wrap_length must be LOWER than or equal to line_length (default: None)
  --isort-multi-line-output ISORT_MULTI_LINE_OUTPUT
                        Multi line output (0-grid, 1-vertical, 2-hanging, 3-vert-hanging, 4-vert-grid, 5-vert-grid-grouped, 6-deprecated-alias-for-5, 7-noqa, 8-vertical-hanging-indent-bracket, 9-vertical-prefix-from-module-import, 10-hanging-indent-with-parentheses). (default: 5)
  --isort-known-third-party ISORT_KNOWN_THIRD_PARTY
                        Force isort to recognize a module as being part of a third party library. (default: None)
  --isort-known-first-party ISORT_KNOWN_FIRST_PARTY
                        Force isort to recognize a module as being part of the current python project. (default: None)
  --isort-known-local-folder ISORT_KNOWN_LOCAL_FOLDER
                        Force isort to recognize a module as being a local folder. Generally, this is reserved for relative imports (from . import module). (default: None)
  --isort-virtual-env ISORT_VIRTUAL_ENV
                        virtual env path (default: /Users/dizballanze/apps/gray/env)
  --isort-include-trailing-comma ISORT_INCLUDE_TRAILING_COMMA
                        Includes a trailing comma on multi line imports that include parentheses. (default: True)
  --isort-lines-after-imports ISORT_LINES_AFTER_IMPORTS
                        empty lines after imports (default: 2)
  --isort-skip-gitignore ISORT_SKIP_GITIGNORE
                        Treat project as a git repository and ignore files listed in .gitignore. (default: True)
  --isort-use-parentheses ISORT_USE_PARENTHESES
                        Use parentheses for line continuation on length limit instead of slashes. **NOTE**: This is separate from wrap modes, and only affects how individual lines that are too long get continued, not sections of multiple imports.. (default: True)
  --isort-length-sort ISORT_LENGTH_SORT
                        Sort imports by their string length. (default: False)
  --isort-add-imports ISORT_ADD_IMPORTS
                        Adds the specified import lines to all files, automatically determining correct placement. (default: None)
  --isort-remove-imports ISORT_REMOVE_IMPORTS
                        Removes the specified imports from all files. (default: None)

autoflake options:
  --autoflake-ignore-init-module-imports AUTOFLAKE_IGNORE_INIT_MODULE_IMPORTS
  --autoflake-expand-star-imports AUTOFLAKE_EXPAND_STAR_IMPORTS
  --autoflake-remove-all-unused-imports AUTOFLAKE_REMOVE_ALL_UNUSED_IMPORTS
  --autoflake-remove-duplicate-keys AUTOFLAKE_REMOVE_DUPLICATE_KEYS
  --autoflake-remove-unused-variables AUTOFLAKE_REMOVE_UNUSED_VARIABLES
  --autoflake-remove-rhs-for-unused-variables
                        remove RHS of statements when removing unused variables (unsafe) (default: False)

trim options:
  --trim-leading-newlines TRIM_LEADING_NEWLINES

fixit options:
  --fixit-redundant-fstrings FIXIT_REDUNDANT_FSTRINGS
  --fixit-redundant-lambdas FIXIT_REDUNDANT_LAMBDAS
  --fixit-redundant-list-comprehensions FIXIT_REDUNDANT_LIST_COMPREHENSIONS
  --fixit-to-comprehensions FIXIT_TO_COMPREHENSIONS
  --fixit-to-literals FIXIT_TO_LITERALS
  --fixit-to-fstrings FIXIT_TO_FSTRINGS

black options:
  --black-line-length BLACK_LINE_LENGTH
                        How many characters per line to allow. (default: 88)
  --black-skip-magic-trailing-comma BLACK_SKIP_MAGIC_TRAILING_COMMA
                        Don't use trailing commas as a reason to split lines. (default: False)
  --black-skip-string-normalization BLACK_SKIP_STRING_NORMALIZATION
                        Don't normalize string quotes or prefixes. (default: False)

Args that start with '--' can also be set in a config file (/Users/dizballanze/.gray or /etc/gray.conf or ./gray.conf). Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi). In general, command-line values override config file values which override defaults.
```


## Git Hook

You can setup gray formatting before each commit with pre-commit git hook.
Add following file to `.git/hooks/pre-commit` and make it executable with
`chmod +x .git/hooks/pre-commit`.

```python
#!/usr/bin/env python
from gray.hooks import git_pre_commit

exit(git_pre_commit(stop_on_modify=True))
```

If `stop_on_modify` argument is `True`, hook will prevent commit if there are
any unstaged changes in files you about to commit.

Otherwise, any unstaged changes in this files will be added to the index
by the hook.


## Config file

Gray is looking for config file in `./gray.conf`, `/etc/gray.conf` or `~/.gray`.

Example of grayconf:

```
formatters = add-trailing-comma,isort,string_fixer
min-python-version = 3.12
```

## Features

* TODO

## Git pre-commit hook

Use [pre-commit](https://pre-commit.com/). Once you
[have it installed](https://pre-commit.com/#install), add this to the
`.pre-commit-config.yaml` in your repository:

```yaml
repos:
  - repo: https://github.com/dizballanze/gray
    rev: master # Replace by any tag/branch: https://github.com/dizballanze/gray/tags
    hooks:
      - id: gray
```

and run `pre-commit install`.

## Using with Sourcetree
Sourcetree may run without `gray` being available via `PATH`.

### MacOS
Make sure `gray` is available via `PATH` and run `open /Applications/Sourcetree.app`.
Or better [create](https://stackoverflow.com/a/281455/1555653) an `Automator` workflow 
with `source ~/.bash_profile && open /Applications/Sourcetree.app` script.
