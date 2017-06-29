from distutils.core import setup

setup(
    name='airconditioner',
    version='0.5.0',
    py_modules=['airconditioner', 'constructors'],
    url='https://github.com/wooga/bit.airconditioner',
    license='',
    author='',
    author_email='bit-admin@wooga.com',
    description='Yaml based DAG configurator for airflow',
    install_requires=[
        "pyyaml",
        "airflow>=1.7.1.3",
    ],
    extras_require={
        'dev': ['behave'],
    },
)
