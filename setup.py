import os
from setuptools import setup, find_packages  # noqa: H301

NAME = "svix-ksuid"
VERSION = "0.4.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "python-baseconv",
]

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=NAME,
    version=VERSION,
    description=" A pure-Python KSUID implementation",
    author="Svix",
    author_email="development@svix.com",
    url="https://www.svix.com",
    license="MIT",
    keywords=[
        "svix",
        "ksuid",
    ],
    python_requires=">=3.6",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description=README,
    long_description_content_type="text/markdown",
)
