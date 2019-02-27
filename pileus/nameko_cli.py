from nameko.runners import ServiceRunner
import eventlet
eventlet.monkey_patch()  # noqa (code before rest of imports)

import logging
import re, os
from functools import partial

import yaml

from nameko.exceptions import CommandError, ConfigurationError

ENV_VAR_MATCHER = re.compile(
    r"""
        \$\{       # match characters `${` literally
        ([^}:\s]+) # 1st group: matches any character except `}` or `:`
        :?         # matches the literal `:` character zero or one times
        ([^}]+)?   # 2nd group: matches any character except `}`
        \}         # match character `}` literally
    """, re.VERBOSE
)

IMPLICIT_ENV_VAR_MATCHER = re.compile(
    r"""
        .*          # matches any number of any characters
        \$\{.*\}    # matches any number of any characters
                    # between `${` and `}` literally
        .*          # matches any number of any characters
    """, re.VERBOSE
)

def _replace_env_var(match):
    env_var, default = match.groups()
    value = os.environ.get(env_var, None)
    if value is None:
        # expand default using other vars
        if default is None:
            # regex module return None instead of
            #  '' if engine didn't entered default capture group
            default = ''

        value = default
        while IMPLICIT_ENV_VAR_MATCHER.match(value):  # pragma: no cover
            value = ENV_VAR_MATCHER.sub(_replace_env_var, value)
    return value

def env_var_constructor(loader, node, raw=False):
    raw_value = loader.construct_scalar(node)
    value = ENV_VAR_MATCHER.sub(_replace_env_var, raw_value)
    return value if raw else yaml.safe_load(value)


def setup_yaml_parser():
    yaml.add_constructor('!env_var', env_var_constructor)
    yaml.add_constructor('!raw_env_var',
                         partial(env_var_constructor, raw=True))
    yaml.add_implicit_resolver('!env_var', IMPLICIT_ENV_VAR_MATCHER)

def run(config, *svcs):
    from sys import argv
    setup_yaml_parser()
    config = yaml.load(open(argv[1]))
    logging.info(config)
    runner = ServiceRunner(config = config)

    for svc in svcs:
        runner.add_service(svc)
    runner.start()

    runnlet = eventlet.spawn(runner.wait)

    while True:
        try:
            runnlet.wait()
        except OSError as exc:
            if exc.errno == errno.EINTR:
                # this is the OSError(4) caused by the signalhandler.
                # ignore and go back to waiting on the runner
                continue
            raise
        except KeyboardInterrupt:
            print()  # looks nicer with the ^C e.g. bash prints in the terminal
            try:
                runner.stop()
            except KeyboardInterrupt:
                print()  # as above
                runner.kill()
        else:
            # runner.wait completed
            break
