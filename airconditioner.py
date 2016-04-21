from os import path

from configure import Configuration, ConfigurationError
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.exasol_operator import ExasolOperator
from airflow.operators.sensors import TimeDeltaSensor, SleepSensor, SqlSensor, ExternalTaskSensor
import logging


def date_to_datetime(args):
    date_attrs = ['start_date', 'end_date']

    for attr in date_attrs:
        if args.get(attr):
            args[attr] = datetime(args[attr].year, args[attr].month, args[attr].day)

    return args


class Config(object):
    _base_path = path.join(path.abspath(path.dirname(__file__)), path.pardir, 'config')

    @classmethod
    def __load(cls, file_path):
        return Configuration.from_file(file_path).configure()

    def __init__(self, yaml_path=None, file_name=None, conf=None):
        """
        :type file_path: str
        :type conf: Configuration
        """
        if yaml_path is None:
            yaml_path = self._base_path
        if file_name is not None:
            file_path = path.join(yaml_path, file_name)

            try:
                self.conf = self.__load(file_path)
            except ConfigurationError:
                # TODO: better handle empty file errors
                self.conf = {}
                pass

        if conf is not None:
            assert isinstance(conf, object)
            self.conf = conf

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

    def chain(self, tasks):
        deltas = [obj for _, obj in tasks.items() if type(obj) == task_types['time_delta']]
        deltas.sort(key=lambda delta: delta.delta)

        for this_delta, next_delta in zip(deltas, deltas[1:]):
            this_delta.set_downstream(next_delta)


class GameConfig(Config):
    def __init__(self, game=None, conf=None, parent=None, yaml_path=None):
        file_name = 'games.yaml' if conf is None else None
        super(GameConfig, self).__init__(file_name=file_name, conf=conf, yaml_path=yaml_path)

        if game is not None:
            self.game = game
            self.parent = parent
            self.conf = self.conf.get(game, {})
        else:
            self.game = None
            self.parent = None

    @property
    def platform(self):
        return self.conf['platform']

    @property
    def profile(self):
        return self.conf.get('profile', 'default')

    @property
    def params(self):
        parent_params = self.parent.conf.get('default', {}).get('params', {}) or {}
        params = self.conf.get('params', {}) or {}
        parent_params.update(params)
        return dict(parent_params)

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


task_types = {
    'time_delta': TimeDeltaSensor,
    'exasol': ExasolOperator,
    'sleep': SleepSensor,
    'sql_sensor': SqlSensor,
    'task': ExternalTaskSensor,
    'dummy': DummyOperator,
}


class TaskConfig(Config):

    def __init__(self, conf=None, yaml_path=None):
        file_name = 'tasks.yaml' if conf is None else None
        super(TaskConfig, self).__init__(file_name=file_name, conf=conf, yaml_path=yaml_path)

    def compile_tasks(self, dag, game_config, deps_config, cluster_config):
        tasks = {}
        time_delta = TimeDelta(dag)

        for cluster, cluster_options in game_config.clusters.items():
            cluster_options = date_to_datetime(cluster_options or {})
            for task_id in cluster_config.get_tasks(cluster):
                if not dag.has_task(task_id):
                    result = self.resolve(dag, task_id, game_config, cluster_options)
                    if result:
                        tasks[task_id] = result

        deps_config.apply_deps(tasks)
        time_delta.chain(tasks)

        return tasks

    def get_task_config(self, task_id, profile, platform):
        task_config = self.conf.get(task_id)

        if not task_config:
            logging.warn("No configuration found for task '%s'" % task_id)
            return None

        task_config = task_config.get(profile, task_config.get('default'))  # ASK ABOUT THIS AND YAML

        if not task_config:
            logging.warn("No configuration found for task '%s' and profile '%s'" % (task_id, profile))
            return None

        # resolve task configuration by platform
        platform_task_config = task_config.get(platform)

        if not platform_task_config:
            platform_task_config = task_config.get('default')

        if not platform_task_config:
            logging.warn("No configuration found for task '%s' and platform '%s'" % (task_id, platform))
            return None

        return platform_task_config

    def resolve(self, dag, task_id, game_config, cluster_options):
        """
        :param dag:
        :type dag: airflow.models.DAG
        :param task_id:
        :type: string
        :param game_config:
        :type: GameConfig
        :param cluster_options:
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
        task_args = cluster_options
        task_args.update({'params': params, 'dag': dag, 'task_id': task_id})

        task_config = self.get_task_config(task_id, profile, platform)

        if not task_config:
            return None

        task_type = None

        for k, v in task_config.items():
            if k == 'type':
                task_type = v
            else:
                task_args[k] = v

        if not type:
            raise Exception("no type specified for task '%s'" % task_id)

        return self.make_task(task_type, task_args)

    @classmethod
    def make_task(cls, task_type, params):
        if task_type not in task_types:
            raise Exception("task type '%s' not defined" % task_type)
        return task_types[task_type](**params)


class DepConfig(Config):
    def __init__(self, conf=None, yaml_path=None):
        """
        :type conf: Configuration
        """
        file_name = 'dependencies.yaml' if conf is None else None
        super(DepConfig, self).__init__(file_name=file_name, conf=conf, yaml_path=yaml_path)

    def get_deps(self, task_id):
        return self.conf.get(task_id, {})

    def apply_deps(self, tasks):

        for main_task_id, main_task in tasks.items():
            for dep_task_id in self.get_deps(main_task_id):
                dep = tasks.get(dep_task_id)
                if dep:
                    main_task.set_upstream(dep)


class DAGBuilder(object):
    def __init__(self, conf=None, yaml_path=None):
        """
        :param conf:
        :type: Configuration
        """
        if conf is not None:
            self.game_config = GameConfig(conf=conf.games)
            self.deps_config = DepConfig(conf=conf.dependencies)
            self.cluster_config = ClusterConfig(conf=conf.clusters)
            self.task_config = TaskConfig(conf=conf.tasks)
        else:
            self.deps_config = DepConfig(yaml_path=yaml_path)
            self.cluster_config = ClusterConfig(yaml_path=yaml_path)
            self.task_config = TaskConfig(yaml_path=yaml_path)
            self.game_config = GameConfig(yaml_path=yaml_path)

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
            self.task_config.compile_tasks(dag, game_config, self.deps_config, self.cluster_config)
            dags[dag.dag_id] = dag

        if target:
            target.update(dags)

        return dags
