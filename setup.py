from setuptools import setup

requires = [
    'Flask-SQLAlchemy',
    'Flask',
    'alembic',
    'psycopg2-binary',
    ]

setup(
    name="jurge",
    version="0.1",
    description="Jurge",
    packages=["jurge"],
    package_dir={"": "."},
    include_package_data=True,
    test_suite="jurge",
    install_requires=requires,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "jurge = jurge.server:run",
        ]})
