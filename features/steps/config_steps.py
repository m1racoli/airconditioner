from behave import *
import yaml
import constructors


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
    constructors.load()
    context.yaml_config = yaml.load(context.yaml_config)


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
