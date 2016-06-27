from datetime import datetime

import sys
import yaml
from behave import *

from airconditioner import DAGBuilder, task_types


def assert_equals(actual, expected):
    assert actual == expected, "expected %s, but got %s" % (expected, actual)


def assert_contains(l, item):
    assert item in l, "%s not found in %s" % (item, l)


def assert_does_not_contain(l, item):
    assert item not in l, "%s found in %s" % (item, l)


def assert_contains_task_id(l, item):
    assert item in [i.task_id for i in l], "%s not found in %s" % (item, l)


def get_dag(context, dag_id):
    dag = context.dags.get(dag_id)
    if dag:
        return dag
    raise Exception('DAG %s not found' % dag_id)


def get_task(dag, task_id):
    for x in dag.tasks:
        if x.task_id == task_id:
            return x
    return None


@given(u'We have an empty configuration')
def step_impl(context):
    context.dag_config = {
        'clusters': {},
        'dependencies': {},
        'games': {},
        'tasks': {},
    }


@when(u'I build the DAGs')
def step_impl(context):
    yaml_string = yaml.safe_dump(context.dag_config, default_style='"').replace('"', '')
    config = yaml.load(yaml_string)
    context.dags = DAGBuilder(conf=config).build()


@when(u'I try to build the DAGs')
def step_impl(context):
    yaml_string = yaml.safe_dump(context.dag_config, default_style='"').replace('"', '')
    config = yaml.load(yaml_string)
    try:
        context.dags = DAGBuilder(conf=config).build()
    except Exception:
        context.exception = {'type': sys.exc_info()[0].__name__, 'msg': sys.exc_info()[1]}
        pass


@then(u'There are no DAGs')
def step_impl(context):
    assert_equals(len(context.dags), 0)


@given(u'The game config contains the item "{game}"')
def step_impl(context, game):
    context.dag_config['games'][game] = {}
    context.dag_config['games'][game]['clusters'] = {}


@then(u'There is {cnt:d} DAG')
def step_impl(context, cnt):
    assert_equals(len(context.dags), cnt)


@then(u'The DAG "{game_id}" is empty')
def step_impl(context, game_id):
    context.execute_steps(u'Then The DAG "{game}" has {cnt} tasks'.format(game=game_id, cnt=0))


@step('There is a cluster "{cluster}"')
def step_impl(context, cluster):
    """
    :type cluster: str
    :type context: behave.runner.Context
    """
    context.dag_config['clusters'][cluster] = []


@given('The cluster "{cluster}" has the task "{task}"')
def step_impl(context, cluster, task):
    """
    :type cluster: str
    :type task: str
    :type context: behave.runner.Context
    """
    cluster_config = context.dag_config['clusters'][cluster]
    if task not in cluster_config:
        cluster_config.append(task)


@given('The cluster "{cluster}" has a task "{task_id}" with the argument "{key}" set as "{value}"')
def step_impl(context, cluster, task_id, key, value):
    """
    :type key: str
    :type value: str
    :type cluster: str
    :type task_id: str
    :type context: behave.runner.Context
    """

    item = {task_id: {key: value}}
    cluster_config = context.dag_config['clusters'][cluster]

    for task in cluster_config:
        if isinstance(task, dict):
            item[task_id].update(task.get(task_id, {}))
        if task == task_id:
            cluster_config.remove(task)

    cluster_config.append(item)


@given('The game "{game}" has the cluster "{cluster}"')
def step_impl(context, game, cluster):
    """
    :type game: str
    :type cluster: str
    :type context: behave.runner.Context
    """
    context.dag_config['games'][game]['clusters'][cluster] = {}


@given('The game "{game}" has the platform "{platform}"')
def step_impl(context, game, platform):
    """
    :type game: str
    :type platform: str
    :type context: behave.runner.Context
    """
    context.dag_config['games'][game]['platform'] = platform


@given('The game "{game}" has the profile "{profile}"')
def step_impl(context, game, profile):
    """
    :type game: str
    :type profile: str
    :type context: behave.runner.Context
    """
    context.dag_config['games'][game]['profile'] = profile


@step('The DAG "{game}" has {cnt:d} tasks')
def step_impl(context, game, cnt):
    """
    :type game: str
    :param cnt: integer
    :type context: behave.runner.Context
    """
    assert_equals(len(get_dag(context, game).tasks), cnt)


@step('The DAG "{game}" has the task "{task}"')
def step_impl(context, game, task):
    """
    :type game: str
    :type task: str
    :type context: behave.runner.Context
    """
    assert_contains_task_id(get_dag(context, game).tasks, task)


@given('The task "{task}" is a {task_type} operator as default')
def step_impl(context, task, task_type):
    """
    :type task: str
    :type task_type: str
    :type context: behave.runner.Context
    """
    context.dag_config['tasks'][task] = {'default': {'default': {'type': task_type}}}


@given("There are minimum default arguments specified")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    conf = context.dag_config['games'].get('default')
    if conf is None:
        context.dag_config['games']['default'] = {}
        conf = context.dag_config['games']['default']

    conf['default_args'] = {
        'owner': 'deploy',
        'start_date': datetime.now()
    }


@given('The task "{task_upstream}" is dependency of the task "{task_downstream}"')
def step_impl(context, task_upstream, task_downstream):
    """
    :type task_upstream: str
    :type task_downstream: str
    :type context: behave.runner.Context
    """

    dep = context.dag_config['dependencies'].get(task_downstream)
    if dep is None:
        context.dag_config['dependencies'][task_downstream] = []
    dep = context.dag_config['dependencies'].get(task_downstream)

    dep.append(task_upstream)


@given('The task "{task_upstream}" is an optional dependency of the task "{task_downstream}"')
def step_impl(context, task_upstream, task_downstream):
    """
    :type task_upstream: str
    :type task_downstream: str
    :type context: behave.runner.Context
    """

    dep = context.dag_config['dependencies'].get(task_downstream)
    if dep is None:
        context.dag_config['dependencies'][task_downstream] = []
    dep = context.dag_config['dependencies'].get(task_downstream)

    dep.append("(%s)" % task_upstream)


@step('In the DAG "{dag_id}" the task "{task_upstream}" is dependency of "{task_downstream}"')
def step_impl(context, dag_id, task_upstream, task_downstream):
    """
    :type dag_id: str
    :type task_upstream: str
    :type task_downstream: str
    :type context: behave.runner.Context
    """
    dag = get_dag(context, dag_id)
    upstream = get_task(dag, task_upstream)
    downstream = get_task(dag, task_downstream)
    assert_contains(upstream.downstream_list, downstream)
    assert_contains(downstream.upstream_list, upstream)


@then('The parameter "{param_key}" of the task "{task_id}" in DAG "{dag_id}" equals "{param_value}"')
def step_impl(context, param_key, task_id, dag_id, param_value):
    """
    :type param_value: str
    :type param_key: str
    :type task_id: str
    :type dag_id: str
    :type context: behave.runner.Context
    """
    dag = get_dag(context, dag_id)
    task = get_task(dag, task_id)
    assert_equals(task.params.get(param_key), param_value)


@given('The game "{game_id}" has the {item_type} "{key}" set as "{value}"')
def step_impl(context, game_id, item_type, key, value):
    """
    :type game_id: str
    :type item_type: str
    :type key: str
    :type value: str
    :type context: behave.runner.Context
    """
    if item_type == 'parameter':
        t = 'params'
    elif item_type == 'argument':
        t = 'default_args'
    else:
        raise Exception('unkknow type %s' % item_type)

    conf = context.dag_config['games'].get(game_id)
    if conf is None:
        context.dag_config['games'][game_id] = {}
        conf = context.dag_config['games'][game_id]

    params = conf.get(t)
    if params is None:
        conf[t] = {}
        params = conf[t]

    params[key] = value


@then('The attribute "{attr}" of the task "{task_id}" in DAG "{dag_id}" equals "{value}"')
def step_impl(context, attr, task_id, dag_id, value):
    """
    :type attr: str
    :type task_id: str
    :type dag_id: str
    :type value: str
    :type context: behave.runner.Context
    """
    dag = get_dag(context, dag_id)
    task = get_task(dag, task_id)
    assert_equals(getattr(task, attr), value)


@given('The cluster "{cluster_id}" for the game "{game_id}" has the argument "{key}" set as "{value}"')
def step_impl(context, cluster_id, game_id, key, value):
    """
    :type cluster_id: str
    :type game_id: str
    :type key: str
    :type value: str
    :type context: behave.runner.Context
    """
    conf = context.dag_config['games'].get(game_id)
    if conf is None:
        context.dag_config['games'][game_id] = {}
        conf = context.dag_config['games'][game_id]

    cluster = conf.get('clusters').get(cluster_id)
    if cluster is None:
        conf.get('clusters')[cluster_id] = {}
        cluster = conf.get('clusters')[cluster_id]

    cluster[key] = value


@step('The task "{task_id}" is a {task_type} operator for profile "{profile}" and platform "{platform}"')
def step_impl(context, task_id, task_type, profile, platform):
    """
    :type task_id: str
    :type task_type: str
    :type profile: str
    :type platform: str
    :type context: behave.runner.Context
    """
    task_config = context.dag_config['tasks'].get(task_id)

    if task_config is None:
        context.dag_config['tasks'][task_id] = {}
        task_config = context.dag_config['tasks'][task_id]

    profile_config = task_config.get(profile)

    if profile_config is None:
        task_config[profile] = {}
        profile_config = task_config[profile]

    profile_config[platform] = {'type': task_type}


@then('The DAG "{dag_id}" has the task "{task_id}" as a {task_type} operator')
def step_impl(context, dag_id, task_id, task_type):
    """
    :type dag_id: str
    :type task_id: str
    :type task_type: str
    :type context: behave.runner.Context
    """
    dag = get_dag(context, dag_id)
    assert_contains(dag.task_ids, task_id)
    task = get_task(dag, task_id)
    assert_equals(type(task), task_types[task_type])


@step(
    'The task "{task_id}" for profile "{profile}" and platform "{platform}" has the argument "{key}" set to "{value}"')
def step_impl(context, task_id, profile, platform, key, value):
    """
    :type task_id: str
    :type profile: str
    :type platform: str
    :type key: str
    :type value: str
    :type context: behave.runner.Context
    """
    task_config = context.dag_config['tasks'].get(task_id)

    if task_config is None:
        context.dag_config['tasks'][task_id] = {}
        task_config = context.dag_config['tasks'][task_id]

    profile_config = task_config.get(profile)

    if profile_config is None:
        task_config[profile] = {}
        profile_config = task_config[profile]

    platform_config = profile_config.get(platform)

    if platform_config is None:
        profile_config[platform] = {}
        platform_config = profile_config[platform]

    platform_config[key] = value


@step('In the DAG "{dag_id}" the task "{task_a}" is not dependency of "{task_b}"')
def step_impl(context, dag_id, task_a, task_b):
    """
    :param task_b:
    :param task_a:
    :type dag_id: str
    :type context: behave.runner.Context
    """
    dag = get_dag(context, dag_id)
    task_a = get_task(dag, task_a)
    task_b = get_task(dag, task_b)
    assert_does_not_contain(task_a.downstream_list, task_b)
    assert_does_not_contain(task_b.upstream_list, task_a)


@given('I have a set of YAMLs located at "{path}"')
def step_impl(context, path):
    """
    :type path: str
    :type context: behave.runner.Context
    """
    context.path = path


@when("I build the DAGs from those YAMLs")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.dags = DAGBuilder(yaml_path=context.path).build()


@then('The attribute "{attr}" of the task "{task_id}" in DAG "{dag_id}" is of type "{value_type}"')
def step_impl(context, attr, task_id, dag_id, value_type):
    """
    :param dag_id:
    :type attr: str
    :type task_id: str
    :type value_type: str
    :type context: behave.runner.Context
    """
    dag = get_dag(context, dag_id)
    task = get_task(dag, task_id)
    assert_equals(type(getattr(task, attr)).__name__, value_type)


@when('I build the DAGs with the ids "{dag_ids}"')
def step_impl(context, dag_ids):
    """
    :type dag_ids: str
    :type context: behave.runner.Context
    """
    dag_ids = dag_ids.split(',')
    yaml_string = yaml.safe_dump(context.dag_config, default_style='"').replace('"', '')
    config = yaml.load(yaml_string)
    context.dags = DAGBuilder(conf=config).build(dag_ids=dag_ids)


@then('There is no task "{task_id}" in the DAG "{dag_id}"')
def step_impl(context, task_id, dag_id):
    """
    :type task_id: str
    :type dag_id: str
    :type context: behave.runner.Context
    """
    dag = get_dag(context, dag_id)
    task = get_task(dag, task_id)
    assert_equals(task, None)


@step("There hasn't been an exception")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    e = getattr(context, "exception", None)
    assert_equals(e, None)


@then('There has been an exception "{exception_type}"')
def step_impl(context, exception_type):
    """
    :type exception_type: str
    :type context: behave.runner.Context
    """
    e = getattr(context, "exception", {})
    assert_equals(e.get('type'), exception_type)
    print(e.get('msg'))


@then('The task "{task_id}" in the DAG "{dag_id}" is a {operator_type} operator as default')
def step_impl(context, task_id, dag_id, operator_type):
    """
    :param task_id:
    :type dag_id: str
    :type operator_type: str
    :type context: behave.runner.Context
    :type operator_type: str
    """

    dag = get_dag(context, dag_id)
    task = get_task(dag, task_id)
    assert_equals(type(task).__name__, operator_type)


@then('The start_date of the task "{task_id}" in DAG "{dag_id}" equals "{value}"')
def step_impl(context, task_id, dag_id, value):
    """
    :type task_id: str
    :type dag_id: str
    :type value: str
    :type context: behave.runner.Context
    """
    dag = get_dag(context, dag_id)
    task = get_task(dag, task_id)
    assert_equals(datetime.strftime(getattr(task, "start_date"),"%Y-%m-%d"), value)
