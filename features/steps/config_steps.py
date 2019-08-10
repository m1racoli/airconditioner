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

from behave import *
import yaml


@given("We have an empty yaml configuration")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.yaml_config = ""


@given('The line "{line}" has been appended to the YAML config')
def step_impl(context, line):
    """
    :type context: behave.runner.Context
    :param line:
    :type line: str
    """
    context.yaml_config += line + '\n'


@when("I load the YAML config")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.yaml_config = yaml.load(context.yaml_config, Loader=yaml.Loader)


@then('The type of "{key}" is a "{value_type}"')
def step_impl(context, key, value_type):
    """
    :type key: str
    :type value_type: str
    :type context: behave.runner.Context
    """
    assert_equals(type(context.yaml_config[key]).__name__, value_type)


@then('The function "{key}" evaluates "{input}" to "{output}"')
def step_impl(context, key, input, output):
    """
    :type context: behave.runner.Context
    :type in: str
    :type out: str
    """
    assert_equals(context.yaml_config[key](input), output)


@then('The object "{key}" prints to "{output}"')
def step_impl(context, key, output):
    """
    :type context: behave.runner.Context
    :type str: str
    """
    assert_equals(context.yaml_config[key].__str__(), output)


def assert_equals(actual, expected):
    assert actual == expected, "expected %s, but got %s" % (expected, actual)
