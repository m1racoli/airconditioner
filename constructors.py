import re
from datetime import timedelta

import yaml


__timedelta_regex = re.compile(
    r'((?P<weeks>\d+?)w)?((?P<days>\d+?)d)?((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')


def __timedelta_constructor(loader, node):
    value = loader.construct_scalar(node)
    parts = __timedelta_regex.match(value)
    if not parts:
        return timedelta()
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.iteritems():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)


def __lambda_constructor(loader, node):
    value = loader.construct_scalar(node)
    return eval("lambda " + value)


def load():
    yaml.add_constructor(u'!timedelta', __timedelta_constructor)
    yaml.add_constructor(u'!lambda', __lambda_constructor)
