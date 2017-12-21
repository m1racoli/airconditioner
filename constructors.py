#
# Copyright 2017 Wooga GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
from datetime import timedelta

import yaml
from future.utils import iteritems

__timedelta_regex = re.compile(
    r'((?P<weeks>\d+?)w)?((?P<days>\d+?)d)?((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')


def __timedelta_constructor(loader, node):
    value = loader.construct_scalar(node)
    parts = __timedelta_regex.match(value)
    if not parts:
        return timedelta()
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in iteritems(parts):
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)


def __lambda_constructor(loader, node):
    value = loader.construct_scalar(node)
    return eval("lambda " + value)


def load():
    yaml.add_constructor(u'!timedelta', __timedelta_constructor)
    yaml.add_constructor(u'!lambda', __lambda_constructor)
