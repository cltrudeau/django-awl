# appmanage.py
#
# Tools for writing a standalone Django app
import argparse
import json
import os
import stat
import sys

from pathlib import Path

import django

from django.conf import settings
from django.core.management.utils import get_random_secret_key

# ===========================================================================

def boot_django(module_dir, test_dir=None, root_url=None, template_dirs=None,
        noawl=False, config_kwargs=None):
    """
    Configures a Django instance including your standalone app. The instance
    is in DEBUG mode with an sqlite3 database.

    :param module_dir:
        Pathlib.Path object pointing to the app's module directory. Adds its
        parent directory to Python's module path.
    :param test_dir:
        (Optional) Pathlib.Path object pointing to directory where tests
        reside.  Adds this directory to Python's module path.
    :param root_url:
        (Optional) Value for the ROOT_URL parameter
    :param template_dirs:
        List of directories for templates. Defaults to `[]`
    :param noawl:
        True to stop the inclusion of the awl library in INSTALLED APPS
    :param config_kwargs:
        A JSON dictionary of keyword arguments to add to the configuration call.
        This should contain any additional definitions you would normally put
        in your settings.py file. Note that this is called as an update to the
        configuration and can be used to overwrite default configuration.
    """
    module_path = Path(module_dir)
    sys.path.insert(0, str(module_path.parent))

    # Base settings for the setup call
    configuration = dict(
        BASE_DIR=module_dir,
        SECRET_KEY='django-insecure-' + get_random_secret_key(),
        DEBUG=True,
        DEFAULT_AUTO_FIELD='django.db.models.AutoField',
        DATABASES={
            'default':{
                'ENGINE':'django.db.backends.sqlite3',
                'NAME': ":memory:",
            }
        },
        MIDDLEWARE=(
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.admin',
            module_path.name,
        ),
        TEMPLATES=[{
            'BACKEND':'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS':True,
            'OPTIONS': {
                'context_processors':[
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ]
            }
        }],
    )

    # Add overrides from the function arguments
    if root_url is not None:
        configuration["ROOT_URLCONF"] = root_url

    if not noawl:
        configuration["INSTALLED_APPS"] += ("awl", )

    if test_dir is not None:
        test_path = Path(test_dir)
        sys.path.insert(0, str(test_path.resolve()))
        configuration["INSTALLED_APPS"] += (test_path.name, )

    if template_dirs is not None:
        configuration["TEMPLATES"]["DIRS"] = template_dirs

    if config_kwargs is not None:
        configuration.update(json.loads(config_kwargs))

    # Configure Django
    settings.configure(**configuration)
    django.setup()

# ===========================================================================
# Implementation of makemanage command

class _Holder:
    pass

def _find_module(src_dir):
    # Utility for finding a single module directory in a given src dir
    count = 0
    mod_dir = None
    for child in src_dir.iterdir():
        if child.is_dir():
            mod_dir = child
            count += 1

    if count == 0:
        raise ValueError(f"Found no module directories in '{src_dir}'")
    elif count != 1:
        raise ValueError((f"Found {count} directories in '{src_dir}' "
            "use --module to specify one of them"))

    return mod_dir


def _make_manage_args(home):
    # Handles arguments for the "makemanage" command
    parser = argparse.ArgumentParser(description=("Generates a manage.py "
        "file for a standalone app"))

    parser.add_argument('--src', help=("Name of the directory that holds the"
        "module definition. If not provided, 'src' is assumed"))

    parser.add_argument('--module', help=("Name of the module to add to the "
        "INSTALLED_APPS settings"))

    parser.add_argument('--test', help=("Name of the directory where tests "
        "can be found. If not provided, looks for 'tests', otherwise "
        "acts as if there are none."))

    parser.add_argument('--noawl', action="store_true", help=("Don't include "
        "awl as in the INSTALLED_APPS configuration"))

    parser.add_argument('--root_url', default=None, help=("Provide a value "
        "for the ROOT_URL setting."))

    parser.add_argument('--template_dirs', default=None, help=("Comma "
        "separated list of directory names where Django looks for templates"))

    parser.add_argument('--config', default=None, help=("JSON dictionary "
        "to be used as **kwargs in the call that defines settings.py values."))

    parser.add_argument('--shebang', default=None, help=("Contents for the "
        "first line in the output script. On systems where os.name returns "
        "'posix', defaults to '#!/usr/bin/env python', otherwise empty"))

    # ----
    # Process arguments
    args = parser.parse_args()
    holder = _Holder()

    if args.src and args.module:
        # "src" directory and module name provided, check the module exists
        mod_dir = (Path(args.src) / Path(args.module)).resolve()
        if not mod_dir.is_dir():
            raise ValueError((f"No module '{args.module}' found in directory "
                f"'{args.src}'"))

        holder.mod_dir = f'"{mod_dir}"'
    elif args.src:
        # "src" but no module name, try to find it
        src_dir = Path(args.src).resolve()
        if not src_dir.is_dir():
            raise ValueError(("No directory named 'src' found. Use --src "
                "to specify a directory"))

        mod_dir = _find_module(src_dir)
        holder.mod_dir = f'"{mod_dir}"'
    else:
        # No src directory, look in home for a "src" folder
        src_dir = home / Path("src")
        if not src_dir.is_dir():
            raise ValueError(("No directory named 'src' found. Use --src "
                "to specify a directory"))

        mod_dir = _find_module(src_dir)
        holder.mod_dir = f'"{mod_dir}"'

    # Check for an optional test directory
    if not args.test:
        path = home / Path("tests")
        if path.is_dir():
            holder.test_dir = f'"{path}"'
        else:
            holder.test_dir = 'None'
    else:
        path = Path(args.test).resolve()
        if Path(args.test).is_dir():
            holder.test_dir = f'"{path}"'
        else:
            raise ValueError(f"Test argument '{args.test}' is not a directory")

    # Handle additional configuration
    holder.noawl = args.noawl
    holder.shebang = args.shebang
    holder.root_url = None
    holder.template_dirs = None
    holder.config = None

    if args.root_url:
        holder.root_url = f'"{args.root_url}"'

    if args.template_dirs:
        holder.template_dirs = args.template_dirs.split(",")

    if args.config:
        holder.config = f'"""{args.config}"""'

    return holder


_MAKE_MANAGE_TEMPLATE = """\
import sys

from awl.appmanage import boot_django

# call the django setup routine
boot_django(
    %s,
    test_dir=%s,
    root_url=%s,
    template_dirs=%s,
    noawl=%s,
    config_kwargs=%s
)

from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)
"""


def _make_manage():
    # Core logic of the "makemanage" script
    FILENAME = "manage.py"
    home = Path.cwd()

    try:
        boot = _make_manage_args(home)
    except ValueError as e:
        print("Error:", e.args[0], file=sys.stderr)
        exit(-1)

    output = _MAKE_MANAGE_TEMPLATE % (boot.mod_dir, boot.test_dir,
        boot.root_url, boot.template_dirs, boot.noawl, boot.config)

    with open(FILENAME, "w") as f:
        if os.name == "posix":
            f.write("#!/usr/bin/env python\n")

        f.write(output)

    if os.name == "posix":
        perms = os.stat(FILENAME).st_mode
        os.chmod(FILENAME, perms | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
