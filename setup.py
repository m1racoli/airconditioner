from distutils.core import setup

setup(
    name='airconditioner',
    version='0.4.1',
    py_modules=['airconditioner', 'constructors'],
    url='https://github.com/wooga/bit.airconditioner',
    license='',
    author='',
    author_email='bit-admin@wooga.com',
    description='Yaml based DAG configurator for airflow',
    install_requires=[
        "behave",
        "pyyaml",
        "airflow",
    ],
)
