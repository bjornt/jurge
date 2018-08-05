from setuptools import setup, find_packages

requires = [
    'graphene[sqlalchemy]',
    #'Flask',
    'Flask-GraphQL',
    'alembic',
    'psycopg2-binary',
    'uwsgi',
    ]


extras_requires_test = [
    'flake8',
    'pytest',
]


setup(
    name="jurge",
    version="0.1",
    description="Jurge",
    packages=find_packages(),
    include_package_data=True,
    test_suite="jurge",
    install_requires=requires,
    tests_require=extras_requires_test,
    extras_require={"test": extras_requires_test},
    entry_points={
        "console_scripts": [
            "jurge = jurge.server:run"
        ]},
)
