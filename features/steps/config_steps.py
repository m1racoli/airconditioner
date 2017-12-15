from behave import *
from configure import Configuration


@given("We have an empty yaml configuration")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.yaml_config = ""


@given('The line "{line}" has been appended to the YAML config')
def step_impl(context, line):
    """
    :type key: str
    :type value: str
    :type context: behave.runner.Context
    """
    context.yaml_config += line + '\n'


@when("I load the YAML config")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.yaml_config = Configuration.from_string(context.yaml_config)


@then('The type of "{key}" is a "{value_type}"')
def step_impl(context, key, value_type):
    """
    :type key: str
    :type value_type: str
    :type context: behave.runner.Context
    """
    assert_equals(type(context.yaml_config[key]).__name__, value_type)


def assert_equals(actual, expected):
    assert actual == expected, "expected %s, but got %s" % (expected, actual)


