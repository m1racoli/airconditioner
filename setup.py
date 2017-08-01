from setuptools import setup

setup(
    name='airconditioner',
    version='0.7.0',
    py_modules=['airconditioner', 'constructors'],
    url='https://github.com/wooga/bit.airconditioner',
    license='',
    author='',
    author_email='bit-admin@wooga.com',
    description='Yaml based DAG configurator for airflow',
    install_requires=[
        "pyyaml",
        "apache-airflow~=1.8",
    ],
    extras_require={
        'dev': ['behave'],
    },
)
