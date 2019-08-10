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

import logging
import re
import yaml
from datetime import datetime
from os import path
from airflow import configuration as airflow_conf
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.sensors import TimeDeltaSensor, SqlSensor, ExternalTaskSensor, TimeSensor

import constructors

# load YAML constructors when importing this module
constructors.load()


def date_to_datetime(args):
    date_attrs = ['start_date', 'end_date']

    for attr in date_attrs:
        if args.get(attr):
            args[attr] = datetime(args[attr].year, args[attr].month, args[attr].day)

    return args


def merge_date(dict_a, dict_b):
    options = {}
    options.update(dict_a)
    for key, value in dict_b.items():
        if dict_a.get(key) and isinstance(value, datetime):
            options[key] = max([dict_a.get(key), value])
        else:
            options[key] = value
    return options


class Config(object):
    _base_path = path.join(path.abspath(path.dirname(__file__)), path.pardir, 'config')

    @classmethod
    def __load(cls, file_path):
        return yaml.load(open(file_path, 'r'), Loader=yaml.Loader)

    def __init__(self, yaml_path=None, file_name=None, conf=None):
        """
        :type yaml_path: str
        :type file_name: str
        :type conf: dict
        """
        if yaml_path is None:
            yaml_path = self._base_path
        elif not path.isabs(yaml_path):
            dags_path = path.expanduser(airflow_conf.get('core', 'DAGS_FOLDER'))
            yaml_path = path.join(dags_path, yaml_path)
        if conf is not None:
            self.conf = conf
        else:
            if file_name is not None:
                file_path = path.join(yaml_path, file_name)
                self.conf = self.__load(file_path)
            else:
                self.conf = {}

                # @classmethod
                # def validate(cls):
                #
                #     dep_tasks = set()
                #     # check if all tasks in 'dependencies' are define in 'tasks'
                #     for task, deps in cls.settings['dependencies'].items():
                #         dep_tasks.add(task)
                #         for dep in deps:
                #             dep_tasks.add(dep)
                #
                #     def_tasks = set()
                #     for task in cls.settings['tasks']:
                #         def_tasks.add(task)
                #
                #     for dep_task in dep_tasks:
                #         if dep_task not in def_tasks:
                #             raise Exception("the task '%s' is not defined" % dep_task)
                #
                #     # TODO implement more validation
                #     pass


# run this file to validate and print the configuration
# if __name__ == "__main__":
#     Config.load()
#     pp = pprint.PrettyPrinter(indent=1)
#     if len(sys.argv) > 1:
#         pp.pprint(Config.settings[sys.argv[1]])
#     else:
#         pp.pprint(Config.settings)


class TimeDelta(object):
    def __init__(self, dag):
        self.dag = dag
        self.deltas = {}

    def get(self, delta, start_time, *args, **kwargs):
        if delta in self.deltas:
            return self.deltas[delta]

        sensor = TimeDeltaSensor(
            delta=delta,
            dag=self.dag,
            start_date=start_time,
            *args,
            **kwargs
        )
        self.deltas[delta] = sensor
        return sensor

    @staticmethod
    def chain(tasks):
        deltas = [obj for _, obj in tasks.items() if type(obj) == system_task_types['time_delta']]
        deltas.sort(key=lambda delta: delta.delta)

        for this_delta, next_delta in zip(deltas, deltas[1:]):
            this_delta.set_downstream(next_delta)


class GameException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GameConfig(Config):
    def __init__(self, game=None, conf=None, parent=None, yaml_path=None):
        file_name = 'games.yaml' if conf is None else None
        super(GameConfig, self).__init__(file_name=file_name, conf=conf, yaml_path=yaml_path)

        if game is not None:
            self.game = game
            self.parent = parent
            self.conf = self.conf.get(game, {})
            self.platform = self.conf.get('platform')

            if not self.platform:
                raise GameException("Game '%s' is missing required attribute 'platform'" % self.game)
        else:
            self.game = None
            self.parent = None

    @property
    def profile(self):
        return self.conf.get('profile', 'default')

    @property
    def params(self):
        result = dict()
        parent_params = self.parent.conf.get('default', {}).get('params', {}) or {}

        params = self.conf.get('params', {}) or {}
        result.update(parent_params)
        result.update(params)
        return result

    @property
    def clusters(self):
        return self.conf.get('clusters', {})

    @property
    def games(self):
        conf = self.conf if self.game is None else self.parent.conf
        return [game for game in conf.keys() if game != 'default']

    @property
    def default_args(self):

        default_args = self.parent.conf.get('default', {}).get('default_args', {}) or {}
        args = self.conf.get('default_args', {}) or {}
        default_args.update(args)

        return date_to_datetime(default_args)


class ClusterConfig(Config):
    def __init__(self, conf=None, yaml_path=None):
        file_name = 'clusters.yaml' if conf is None else None
        super(ClusterConfig, self).__init__(file_name=file_name, conf=conf, yaml_path=yaml_path)

    def get_tasks(self, cluster_id):
        cluster = self.conf.get(cluster_id)
        if not cluster:
            logging.warn("No tasks defined for cluster '%s'" % cluster_id)
        return cluster or {}


system_task_types = {
    'time_sensor': TimeSensor,
    'time_delta': TimeDeltaSensor,
    'sql_sensor': SqlSensor,
    'task': ExternalTaskSensor,
    'bash': BashOperator,
    'dummy': DummyOperator,
    'none': None
}


class NoTaskException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TaskTypeException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TaskConfig(Config):
    def __init__(self, conf=None, yaml_path=None):
        file_name = 'tasks.yaml' if conf is None else None
        super(TaskConfig, self).__init__(file_name=file_name, conf=conf, yaml_path=yaml_path)

    def compile_tasks(self, dag, game_config, deps_config, cluster_config, task_types):
        tasks = {}
        time_delta = TimeDelta(dag)

        for cluster, cluster_options in game_config.clusters.items():
            cluster_options = date_to_datetime(cluster_options or {})
            excluded_tasks = cluster_options.pop('exclude', {})
            for task in cluster_config.get_tasks(cluster):
                options = cluster_options
                if isinstance(task, dict):
                    for task_id, task_options in task.items():
                        options = merge_date(options, date_to_datetime(task_options or {}))
                else:
                    task_id = task

                if task_id not in excluded_tasks and not dag.has_task(task_id):
                    result = self.resolve(dag, task_id, game_config, options, task_types)
                    if result is not None:
                        tasks[task_id] = result

        deps_config.apply_deps(tasks)
        time_delta.chain(tasks)

        return tasks

    def get_task_config(self, task_id, profile, platform):
        task_config = self.conf.get(task_id)

        if not task_config:
            raise NoTaskException("No configuration found for task '%s'" % task_id)

        task_config = task_config.get(profile, task_config.get('default'))

        if not task_config:
            raise NoTaskException("No configuration found for task '%s' and profile '%s'" % (task_id, profile))

        # resolve task configuration by platform
        platform_task_config = task_config.get(platform, task_config.get('default'))

        if not platform_task_config:
            raise NoTaskException("No configuration found for task '%s' and platform '%s'" % (task_id, platform))

        return platform_task_config

    def resolve(self, dag, task_id, game_config, options, task_types):
        """
        :param dag:
        :type dag: airflow.models.DAG
        :param task_id:
        :type: string
        :param game_config:
        :type: GameConfig
        :param options:
        :type: ClusterConfig
        :return:
        :rtype: airflow.models.BaseOperator
        """

        # some standard params
        platform = game_config.platform
        profile = game_config.profile

        # build params available in task instance
        params = game_config.params
        params['game'] = game_config.game
        params['platform'] = platform
        params['profile'] = profile

        # arguments for task constructor
        task_args = dict(options)
        task_args.update({'params': params, 'dag': dag, 'task_id': task_id})
        if task_args.get('start_date'):
            task_args['start_date'] = max(task_args.get('start_date'), game_config.default_args.get('start_date'))

        task_config = self.get_task_config(task_id, profile, platform)

        if not task_config:
            return None

        task_type = None

        for k, v in task_config.items():
            if k == 'type':
                task_type = v
            else:
                task_args[k] = v

        if not task_type:
            raise TaskTypeException(
                "No type specified for task '%s' in platform '%s' and profile '%s'" %
                (task_id, platform, profile)
            )

        return self.make_task(task_type, task_args, task_types)

    @classmethod
    def make_task(cls, task_type, params, task_types):
        if task_type not in task_types:
            raise TaskTypeException(
                "The task type '%s' for task '%s' in platform '%s' and profile '%s' is unknown"
                % (task_type, params['task_id'], params['params']['platform'], params['params']['profile'])
            )

        task_obj = task_types[task_type]
        if task_obj is None:
            return None

        return task_obj(**params)


class DependencyException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DepConfig(Config):
    optional_task_pattern = re.compile(r'\(([a-zA-Z0-9_-]+)\)')

    def __init__(self, conf=None, yaml_path=None):
        """
        :type conf: dict
        """
        file_name = 'dependencies.yaml' if conf is None else None
        super(DepConfig, self).__init__(file_name=file_name, conf=conf, yaml_path=yaml_path)

    def get_deps(self, task_id):
        return map(self.resolve_optional_task, self.conf.get(task_id, {}))

    def apply_deps(self, tasks):
        for main_task_id, main_task in tasks.items():
            for dep_task_id, is_optional in self.get_deps(main_task_id):
                dep = tasks.get(dep_task_id)

                if dep:
                    main_task.set_upstream(dep)
                elif not is_optional:
                    raise DependencyException(
                        "Required task dependency '%s' for task '%s' not found in the DAG '%s'"
                        % (dep_task_id, main_task_id, main_task.dag_id))

    @classmethod
    def resolve_optional_task(cls, task_id):
        match = cls.optional_task_pattern.match(task_id)
        if match is None:
            return task_id, False

        return match.groups()[0], True


class DAGBuilder(object):
    def __init__(self, conf=None, yaml_path=None, custom_task_types=None):
        """
        :param conf:
        :type: dict
        """
        if conf is not None:
            self.game_config = GameConfig(conf=conf['games'])
            self.deps_config = DepConfig(conf=conf['dependencies'])
            self.cluster_config = ClusterConfig(conf=conf['clusters'])
            self.task_config = TaskConfig(conf=conf['tasks'])
        else:
            self.deps_config = DepConfig(yaml_path=yaml_path)
            self.cluster_config = ClusterConfig(yaml_path=yaml_path)
            self.task_config = TaskConfig(yaml_path=yaml_path)
            self.game_config = GameConfig(yaml_path=yaml_path)

        self.task_types = system_task_types.copy()
        for (custom_task_type, custom_operator) in (custom_task_types or {}).items():
            if custom_task_type in system_task_types:
                raise TaskTypeException("the type '%s' is already defined for the operator '%s'" % (custom_task_type, system_task_types[custom_task_type]))
            self.task_types[custom_task_type] = custom_operator

    def build(self, dag_ids=None, target=None):
        """
        Appends tasks and dependencies to the given DAG based on the configuration
        :param target: dictionary to load DAGs into with target[dag_id] = dag
        :type target: dict
        :param dag_ids: DAGs to build, otherwise all defined DAGs
        :type dag_ids: list
        :returns: dictionary of built DAGs
        :rtype: dict
        """

        if not dag_ids:
            dag_ids = self.game_config.games

        dags = {}

        for dag_id in dag_ids:
            game_config = GameConfig(game=dag_id, conf=self.game_config.conf, parent=self.game_config)
            dag = DAG(dag_id, default_args=game_config.default_args)
            self.task_config.compile_tasks(dag, game_config, self.deps_config, self.cluster_config, self.task_types)
            dags[dag.dag_id] = dag

        if target:
            target.update(dags)

        return dags
